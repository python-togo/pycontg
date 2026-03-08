from pydantic import BaseModel, Field
from typing import List
from uuid import UUID


class User(BaseModel):
    username: str = Field(..., title="Username",
                          description="Username of the user")
    email: str = Field(..., title="Email",
                       description="Email address of the user")
    is_active: bool = Field(
        True, title="Is Active", description="Indicates if the user is active"
    )
    is_superuser: bool = Field(
        False, title="Is Superuser", description="Indicates if the user is a superuser"
    )
    is_verified: bool = Field(
        False, title="Is Verified", description="Indicates if the user is verified"
    )


class Proposal(BaseModel):
    format: str = Field(
        ..., title="Format", description="Format of the proposal (e.g., talk, workshop)"
    )
    first_name: str = Field(
        ..., title="First Name", description="First name of the speaker"
    )
    last_name: str = Field(
        ..., title="Last Name", description="Last name of the speaker"
    )
    email: str = Field(..., title="Email",
                       description="Email address of the speaker")
    phone: str = Field(None, title="Phone",
                       description="Phone number of the speaker")
    title: str = Field(..., title="Talk Title",
                       description="Title of the talk")
    level: str = Field(
        ...,
        title="Talk Level",
        description="Level of the talk (beginner, intermediate, advanced)",
    )
    talk_abstract: str = Field(
        ..., title="Talk Abstract", description="Abstract of the talk"
    )
    talk_outline: str = Field(
        ..., title="Talk Outline", description="Outline of the talk"
    )
    bio: str = Field(
        ..., title="Speaker Bio", description="Biography of the speaker"
    )
    needs: bool = Field(
        False, title="Needs", description="Indicates if the speaker has special needs"
    )
    technical_needs: str = Field(
        None,
        title="Technical Needs",
        description="Technical needs for the talk (e.g., projector, microphone)",
    )
    talk_language: str = Field(
        ..., title="Talk Language", description="Language of the talk"
    )
    track: List[str] = Field(
        None, title="Track", description="Track of the talk (e.g., Python, Data Science)"
    )
    accepted: bool = Field(
        False, title="Accepted", description="Indicates if the proposal is accepted"
    )


class SponsorInquiry(BaseModel):
    company: str = Field(..., title="Name", description="Name of the sponsor")
    email: str = Field(..., title="Email",
                       description="Email address of the sponsor")
    website: str = Field(
        ..., title="Company URL", description="URL of the sponsor's company"
    )
    contact: str = Field(
        ..., title="Contact Name", description="Name of the contact person"
    )
    title: str = Field(
        ..., title="Contact Title", description="Title of the contact person"
    )
    phone: str = Field(None, title="Phone",
                       description="Phone number of the sponsor")
    level: str = Field(
        ..., title="Sponsorship Level", description="Level of sponsorship"
    )
    message: str = Field(..., title="Message",
                         description="Message from the sponsor")
    paid: bool = Field(
        False, title="Paid", description="Indicates if the sponsorship is paid"
    )


class VolunteerInquiry(BaseModel):
    first_name: str = Field(
        ..., title="First Name", description="First name of the volunteer"
    )
    last_name: str = Field(
        ..., title="Last Name", description="Last name of the volunteer"
    )
    email: str = Field(..., title="Email",
                       description="Email address of the volunteer")
    phone: str = Field(None, title="Phone",
                       description="Phone number of the volunteer")
    country_city: str = Field(
        ..., title="Country/City", description="Country or city of the volunteer"
    )
    motivation: str = Field(
        ..., title="Message", description="Message from the volunteer"
    )
    availability_before: bool = Field(
        False, title="Availability Before", description="Availability before the event"
    )
    availability_during: bool = Field(
        False, title="Availability During", description="Availability during the event"
    )
    availability_after: bool = Field(
        False, title="Availability After", description="Availability after the event"
    )
    video_editor: bool = Field(
        False, title="Video Editor", description="Indicates if the volunteer is a video editor"
    )
    graphic_designer: bool = Field(
        False, title="Graphic Designer", description="Indicates if the volunteer is a graphic designer"
    )
    other: str = Field(
        None, title="Other", description="Other skills or information from the volunteer"
    )
    accepted: bool = Field(
        False, title="Accepted", description="Indicates if the volunteer is accepted"
    )

    experience: str = Field(
        ..., title="Experience with Python", description="Experience with Python"
    )
    registration: bool = Field(False, title="registration", description="")
    technical: bool = Field(False, title="technical", description="")
    logistic: bool = Field(False, title="logistic", description="")
    social: bool = Field(False, title="social", description="")
    photography: bool = Field(False, title="photography", description="")


class RegistrationInquiry(BaseModel):
    id: str = Field(
        default_factory=UUID, title="ID", description="Unique identifier for the registration"
    )
    fullName: str = Field(
        ..., title="First Name", description="First name of the person registering"
    )
    email: str = Field(
        ..., title="Email", description="Email address of the person registering"
    )
    phone: str = Field(
        None, title="Phone", description="Phone number of the person registering"
    )
    organization: str = Field(
        ..., title="Last Name", description="Last name of the person registering"
    )
    country: str = Field(
        ...,
        title="Country/City",
        description="Country or city of the person registering",
    )
    tshirtsize: str = Field(
        ..., title="T-shirt Size", description="T-shirt size of the person registering"
    )
    dietaryrestrictions: str = Field(
        ..., title="Message", description="Message from the registrant"
    )
    favoritefood: str = Field(
        ..., title="Favorite Food", description="Favorite food of the person registering"
    )
    username: str = Field(
        None, title="Discord Username", description="Discord username of the person registering"
    )
    newsletter: bool = Field(
        False, title="Newsletter", description="Subscribe to the newsletter"
    )
    codeofconduct: bool = Field(
        False, title="Code of Conduct", description="Agree to the code of conduct"
    )


class WaitlistInquiry(BaseModel):
    email: str = Field(
        ..., title="Email", description="Email address of the person on the waitlist"
    )


class SponsorTier(BaseModel):
    name: str = Field(
        ..., title="Name", description="Name of the sponsorship tier"
    )
    title: str = Field(
        ..., title="Title", description="Title of the sponsorship tier"
    )
    availability: int = Field(
        ..., title="Number of pack available", description="Number of pack available"
    )
    available: int = Field(
        ..., title="Number of pack available", description="Number of pack available"
    )
    amount_cfa: int = Field(
        ..., title="Amount in CFA", description="Amount in CFA for the sponsorship tier"
    )
    amount_usd: float = Field(
        ..., title="Amount in USD", description="Amount in USD for the sponsorship tier"
    )
    advantages: List[str] = Field(
        ..., title="Advantages", description="List of advantages for the sponsorship tier"
    )
