/**
 * Schedule Modal Functionality - Updated for individual talk sessions
 * Handles displaying session details in a modal when clicking on session cards
 */

class ScheduleModal {
    constructor() {
        this.modal = null;
        this.sessionData = [];
        this.init();
    }

    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        // Get modal element
        this.modal = document.getElementById('session-modal');
        if (!this.modal) {
            console.error('Session modal not found');
            return;
        }

        // Load session data from script tags
        this.loadData();

        // Setup event listeners
        this.setupEventListeners();
    }

    loadData() {
        try {
            // Load session data
            const sessionDataElement = document.getElementById('session-data');
            if (sessionDataElement) {
                this.sessionData = JSON.parse(sessionDataElement.textContent);
            }
        } catch (error) {
            console.error('Error loading session data:', error);
        }
    }

    setupEventListeners() {
        // Add click listeners to all session cards
        const sessionCards = document.querySelectorAll('.session-card[data-session-id]');
        sessionCards.forEach(card => {
            card.addEventListener('click', (e) => {
                const sessionId = card.dataset.sessionId;
                this.openModal(sessionId);
            });

            // Add keyboard support
            card.setAttribute('tabindex', '0');
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const sessionId = card.dataset.sessionId;
                    this.openModal(sessionId);
                }
            });
        });

        // Close modal event listeners
        const closeButton = this.modal.querySelector('.modal-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => this.closeModal());
        }

        // Close modal when clicking outside
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.style.display !== 'none') {
                this.closeModal();
            }
        });
    }

    openModal(sessionId) {
        const session = this.sessionData.find(s => s.id === sessionId);
        if (!session) {
            console.error('Session not found:', sessionId);
            return;
        }

        this.populateModal(session);
        this.showModal();
    }

    populateModal(session) {
        // Set title
        const titleElement = document.getElementById('modal-title');
        if (titleElement) {
            titleElement.textContent = session.title;
        }

        // Set subtitle
        const subtitleElement = document.getElementById('modal-subtitle');
        if (subtitleElement) {
            if (session.subtitle) {
                subtitleElement.textContent = session.subtitle;
                subtitleElement.style.display = 'block';
            } else {
                subtitleElement.style.display = 'none';
            }
        }

        // Set time
        const timeElement = document.getElementById('modal-time');
        if (timeElement) {
            timeElement.textContent = `${session.start_time} – ${session.end_time}`;
        }

        // Set duration
        const durationElement = document.getElementById('modal-duration');
        if (durationElement) {
            durationElement.textContent = `${session.duration} minutes`;
        }

        // Set language tags in modal
        const modalLang = document.getElementById('modal-language');
        if (modalLang) {
            modalLang.innerHTML = '';
            if (session.language && session.language.length > 0) {
                session.language.forEach(lang => {
                    const span = document.createElement('span');
                    span.className = 'language-tag';
                    span.textContent = lang;
                    modalLang.appendChild(span);
                });
            }
        }

        // Set description
        const descriptionElement = document.getElementById('modal-description');
        if (descriptionElement) {
            // Handle line breaks in description
            const description = session.description_full || session.description_short || 'Aucune description disponible.';
            descriptionElement.innerHTML = description.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>');
        }

        // Set speakers
        this.populateSpeakers(session);
    }

    /**
     * CORRECTION: Logique améliorée pour récupérer l'avatar d'un speaker
     */
    getSpeakerAvatar(session, speakerIndex) {
        // 1. Pour les panels et sessions avec multiples speakers, utiliser speaker_details si disponible
        if (session.speaker_details && session.speaker_details[speakerIndex]) {
            return session.speaker_details[speakerIndex].avatar_url;
        }
        
        // 2. Vérifier dans session.panel_avatars (pour les panels et sessions multi-speakers)
        if (session.panel_avatars && session.panel_avatars[speakerIndex]) {
            return session.panel_avatars[speakerIndex];
        }
        
        // 3. Vérifier dans session.avatar_url (pour les sessions individuelles, seulement pour le premier speaker)
        if (speakerIndex === 0 && session.avatar_url) {
            return session.avatar_url;
        }
        
        // 4. Vérifier dans session.talks[speakerIndex] (pour les sessions groupées)
        if (session.talks && session.talks[speakerIndex] && session.talks[speakerIndex].avatar_url) {
            return session.talks[speakerIndex].avatar_url;
        }
        
        // 5. Fallback: pas d'avatar
        return null;
    }

    /**
     * CORRECTION: Gestion des sessions avec multiples speakers (panels et autres)
     */
    handleMultipleSpeakers(session) {
        // Les données sont maintenant correctement passées via speaker_details pour tous les types
        return session.speaker_details || null;
    }

    /**
     * Retrouver les données originales du JSON pour les panels
     */
    findOriginalSessionData(session) {
        // Cette fonction devrait idéalement avoir accès aux données JSON originales
        // Pour l'instant, on peut essayer de deviner si c'est un panel
        if (session.type === 'panel' || session.participant_label === 'panelistes') {
            // Pour les panels, on peut avoir besoin d'accéder aux données JSON originales
            // C'est une limitation de la structure actuelle
            return null;
        }
        return null;
    }

    populateSpeakers(session) {
        const speakersContainer = document.getElementById('modal-speakers');
        if (!speakersContainer) return;

        if (!session.speakers || session.speakers.length === 0) {
            speakersContainer.style.display = 'none';
            return;
        }

        speakersContainer.style.display = 'block';
        
        // CORRECTION: Gestion des sessions avec multiples speakers (pas seulement panels)
        const multipleSpeakers = this.handleMultipleSpeakers(session);
        
        // Create speakers section HTML
        const participantLabel = this.getParticipantLabel(session.participant_label, session.speakers.length);
        
        const speakersHTML = `
            <h4>${participantLabel}</h4>
            <div class="speaker-list">
                ${session.speakers.map((speaker, index) => {
                    // CORRECTION: Utiliser la nouvelle logique pour récupérer l'avatar
                    const avatarUrl = this.getSpeakerAvatar(session, index);
                    
                    const speakerTitle = this.getSpeakerTitle(session.participant_label);
                    
                    // Pour les panels, récupérer les détails spécifiques si disponibles
                    const speakerDetail = session.speaker_details && session.speaker_details[index] ? 
                                        session.speaker_details[index] : null;
                    
                    return `
                        <div class="speaker-item">
                            ${avatarUrl ? 
                                `<img src="${avatarUrl}" alt="${speaker}" class="speaker-avatar" 
                                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />` : 
                                ''
                            }
                            <div class="speaker-avatar" style="${avatarUrl ? 'display: none;' : 'display: flex;'} background: #004225; color: white; align-items: center; justify-content: center; font-weight: bold; font-size: 1rem; width: 60px; height: 60px; border-radius: 50%;">
                                ${speaker.charAt(0)}
                            </div>
                            <div class="speaker-info">
                                <div class="speaker-name">${speaker}</div>
                                <div class="speaker-title">${speakerTitle}</div>
                                ${session.talks && session.talks[index] && session.talks[index].description ? 
                                    `<div class="speaker-talk-desc" style="margin-top: 8px; font-size: 0.85rem; color: #666; font-style: italic;">
                                        ${session.talks[index].description.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>')}
                                    </div>` : 
                                    speakerDetail && speakerDetail.description ?
                                    `<div class="speaker-talk-desc" style="margin-top: 8px; font-size: 0.85rem; color: #666; font-style: italic;">
                                        ${speakerDetail.description.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>')}
                                    </div>` :
                                    ''
                                }
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        speakersContainer.innerHTML = speakersHTML;
    }

    getParticipantLabel(participantLabel, count) {
        const labels = {
            'speaker': count > 1 ? 'Speakers' : 'Speaker',
            'speakers': 'Speakers', 
            'participants': 'Participants',
            'instructors': 'Instructors',
            'experts': 'Experts',
            'panelists': 'Panelists',
            'panelistes': 'Panelists'
        };
        
        // Fallback: si on a plusieurs speakers, utiliser "Speakers"
        if (count > 1 && !labels[participantLabel]) {
            return 'Speakers';
        }
        
        return labels[participantLabel] || (count > 1 ? 'Speakers' : 'Speaker');
    }

    getSpeakerTitle(participantLabel) {
        const titles = {
            'speaker': 'Speaker',
            'speakers': 'Speaker',
            'participants': 'Participant',
            'instructors': 'Instructor',
            'experts': 'Expert',
            'panelists': 'Panelist',
            'panelistes': 'Panelist'
        };
        return titles[participantLabel] || 'Expert·e Python';
    }

    showModal() {
        this.modal.style.display = 'flex';
        // Trigger reflow to ensure display change is registered
        this.modal.offsetHeight;
        this.modal.classList.add('show');
        
        // Focus management for accessibility
        const closeButton = this.modal.querySelector('.modal-close');
        if (closeButton) {
            closeButton.focus();
        }
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.modal.classList.remove('show');
        
        // Wait for animation to complete before hiding
        setTimeout(() => {
            if (!this.modal.classList.contains('show')) {
                this.modal.style.display = 'none';
            }
        }, 300);
        
        // Restore body scroll
        document.body.style.overflow = '';
    }
}

// Initialize the modal when the script loads
new ScheduleModal();
