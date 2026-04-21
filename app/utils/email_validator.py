"""
email_validator.py
------------------
Valide un email sans service tiers :
  1. Format (regex)
  2. Domaine jetable (blocklist)
  3. DNS MX — le domaine a-t-il un vrai serveur mail ?
  4. SMTP RCPT TO — l'adresse complète existe-t-elle ?
     ⚠️  Gmail, Outlook, Yahoo bloquent cette vérification volontairement.
         Ces serveurs répondent toujours OK pour protéger leurs utilisateurs.
         Fonctionne bien sur les petits/moyens serveurs mail.

Dépendance : dnspython
    pip install dnspython
"""

import re
import smtplib
import socket
import dns.resolver
from dataclasses import dataclass


# ── Blocklist des domaines jetables ──────────────────────────────────────────
DISPOSABLE_DOMAINS = {
    "tempmail.com", "tempmail.net", "tempmail.org", "tempmail.de",
    "temp-mail.org", "temp-mail.io", "tempinbox.com",
    "guerrillamail.com", "guerrillamail.net", "guerrillamail.org",
    "guerrillamail.biz", "guerrillamail.de", "guerrillamail.info",
    "grr.la", "guerrillamailblock.com",
    "mailinator.com", "trashmail.com", "trashmail.at", "trashmail.io",
    "trashmail.me", "trashmail.net", "trashmail.org",
    "yopmail.com", "yopmail.fr", "cool.fr.nf", "jetable.fr.nf",
    "nospam.ze.tc", "nomail.xl.cx", "mega.zik.dj", "speed.1s.fr",
    "mailnull.com", "spamgourmet.com", "spam4.me", "sharklasers.com",
    "spam.la", "dispostable.com", "mailnesia.com", "maildrop.cc",
    "throwam.com", "fakeinbox.com", "getnada.com", "discard.email",
    "spamfree24.org", "getairmail.com", "filzmail.com", "tempr.email",
    "spambog.com", "spambog.de", "spambog.ru",
    "0-mail.com", "0815.ru", "0wnd.net", "0wnd.org",
    "10minutemail.com", "10minutemail.net", "10minutemail.org",
    "20minutemail.com", "emailondeck.com", "throwaway.email",
    "spambox.us", "spambox.info", "objectmail.com", "nobulk.com",
    "meltmail.com", "jetable.com", "jetable.net", "jetable.org",
    "inoutmail.net", "inoutmail.info", "inoutmail.eu",
    "hulapla.de", "hailmail.net", "h8s.org", "frapmail.com",
    "fakedemail.com", "despam.it", "deadaddress.com", "burnermail.io",
    "bumpymail.com", "binkmail.com", "antichef.com", "antichef.net",
    "antireg.com", "antireg.ru", "antispam.de", "anonbox.net",
    "anonymbox.com", "anonymail.dk", "anonymize.com",
}

# Domaines qui bloquent le SMTP check (répondent toujours OK)
SMTP_CATCH_ALL_DOMAINS = {
    "gmail.com", "googlemail.com",
    "outlook.com", "hotmail.com", "live.com", "msn.com",
    "yahoo.com", "yahoo.fr", "yahoo.co.uk", "yahoo.es",
    "icloud.com", "me.com", "mac.com",
    "protonmail.com", "proton.me",
    "aol.com",
}

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


# ── Résultat ──────────────────────────────────────────────────────────────────
@dataclass
class ValidationResult:
    email: str
    is_valid: bool
    reason: str
    smtp_checked: bool = False

    def __str__(self):
        status = "✅ Valide" if self.is_valid else "❌ Invalide"
        smtp_note = ""
        if self.is_valid:
            smtp_note = " (SMTP vérifié)" if self.smtp_checked else " (SMTP non vérifiable — grand serveur)"
        return f"{status} — {self.email}\n   → {self.reason}{smtp_note}"


# ── Fonctions internes ────────────────────────────────────────────────────────
def _check_format(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def _check_disposable(domain: str) -> bool:
    return domain.lower() in DISPOSABLE_DOMAINS


def _get_mx_hosts(domain: str) -> list:
    """Retourne la liste des serveurs MX triés par priorité."""
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=5)
        mx_records = sorted(answers, key=lambda r: r.preference)
        return [str(r.exchange).rstrip(".") for r in mx_records]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
            dns.resolver.NoNameservers, dns.exception.Timeout):
        return []


def _smtp_check(email: str, mx_hosts: list) -> tuple:
    """
    Tente une vérification SMTP RCPT TO sans envoyer de mail.

    Retourne (is_valid, was_checked) :
      - is_valid   : True si le serveur confirme que l'adresse existe
      - was_checked: True si le serveur a répondu (False = catch-all ou timeout)
    """
    from_address = "verify@validator.local"

    for mx in mx_hosts[:2]:  # On essaie les 2 premiers MX
        try:
            with smtplib.SMTP(timeout=10) as smtp:
                smtp.connect(mx, 25)
                smtp.ehlo_or_helo_if_needed()
                smtp.mail(from_address)
                code, _ = smtp.rcpt(email)
                smtp.quit()

                if code == 250:
                    return True, True
                elif code == 550:
                    # 550 = utilisateur inexistant confirmé
                    return False, True
                else:
                    continue

        except smtplib.SMTPConnectError:
            continue
        except smtplib.SMTPServerDisconnected:
            continue
        except socket.timeout:
            continue
        except Exception:
            continue

    return True, False  # Pas pu vérifier → on laisse passer


# ── Fonction principale ───────────────────────────────────────────────────────
def validate_email(email: str, smtp: bool = True) -> ValidationResult:
    """
    Valide un email en 4 étapes :
      1. Format
      2. Domaine jetable
      3. DNS MX
      4. SMTP RCPT TO (si smtp=True)

    Paramètre smtp=False pour désactiver le check SMTP (plus rapide).
    """
    email = email.strip().lower()

    # 1. Format
    if not _check_format(email):
        return ValidationResult(email, False, "Format invalide")

    domain = email.split("@")[1]

    # 2. Domaine jetable
    if _check_disposable(domain):
        return ValidationResult(email, False, f"Domaine jetable détecté : {domain}")

    # 3. DNS MX
    mx_hosts = _get_mx_hosts(domain)
    if not mx_hosts:
        return ValidationResult(email, False, f"Aucun serveur mail trouvé pour : {domain}")

    # 4. SMTP check (sauf pour les grands serveurs connus)
    if smtp and domain not in SMTP_CATCH_ALL_DOMAINS:
        is_valid, was_checked = _smtp_check(email, mx_hosts)
        if not is_valid:
            return ValidationResult(email, False, "Adresse email inexistante (SMTP 550)", smtp_checked=True)
        return ValidationResult(email, True, "Format OK · Domaine propre · MX OK · SMTP OK", smtp_checked=was_checked)

    # Grand serveur (Gmail, Outlook...) → impossible de vérifier le username
    return ValidationResult(email, True, "Format OK · Domaine propre · MX OK", smtp_checked=False)


# ── Validation en masse ───────────────────────────────────────────────────────
def validate_emails(emails: list, smtp: bool = True) -> list:
    return [validate_email(e, smtp=smtp) for e in emails]


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_emails = [
        "contact@python.org",            # valide, SMTP vérifiable
        "fakexyz123456@pythonghana.org",      # username inexistant
        "fakeuser99999@gmail.com",       # format ok mais on ne peut pas vérifier
        "test@tempmail.com",             # jetable
        "notanema@pytogo.org",                    # format invalide
        "fake@domaine-inexistant.xyz",   # MX introuvable
    ]

    print("=" * 55)
    print("  Validation d'emails (avec SMTP check)")
    print("=" * 55)
    result = validate_email("test@python.org", smtp=True)
    print(f"{result.is_valid} — {result.email} — {result.reason} (SMTP vérifié: {result.smtp_checked})")
