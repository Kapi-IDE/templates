import os
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend

from app.database import engine, SessionLocal
from app.auth_utils import verify_password
from app.models.user import User, UserRoles, PaymentHistory, Referral, EloHistory
from app.models.quiz import QuizQuestion, QuizSession, Survey, UserAnswer
from app.models.onboarding import OnboardingState, UserOnboardingState
from app.models.programming import ProgrammingChallenge, ProgrammingSession, LearningPod, LearningPodMember
from app.models.learning import  LessonCategory, Lesson, LessonContent, UserLesson, UserLessonIssue
from app.models.workshop import Workshop, WorkshopPaymentHistory

# Custom authentication for SQLAdmin
class AdminAuthentication(AuthenticationBackend):
    async def login(self, request) -> bool:    
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        # Create a database session
        db = SessionLocal()
        try:
            # Find the user with admin role
            user = db.query(User).filter(
                User.username == username,
                User.role == UserRoles.admin,
                User.is_active == True
            ).first()
            
            # Verify the password and admin role
            if user and verify_password(password, user.hashed_password):
                # Store user info in session
                request.session.update({
                    "admin_auth": True,
                    "admin_user_id": user.id,
                    "admin_username": user.username
                })
                return True
            return False
        finally:
            db.close()

    async def logout(self, request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request) -> Optional[bool]:
        return request.session.get("admin_auth", False)

# Create model views for each model
class UserAdmin(ModelView, model=User):
    column_list = [c.key for c in inspect(User).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

class WorkshopAdmin(ModelView, model=Workshop):
    column_list = [c.key for c in inspect(Workshop).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Workshop"
    name_plural = "Workshops"
    icon = "fa-solid fa-calendar-days"

class WorkshopPaymentHistoryAdmin(ModelView, model=WorkshopPaymentHistory):
    column_list = [c.key for c in inspect(WorkshopPaymentHistory).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Workshop Payment History"
    name_plural = "Workshop Payment History"
    icon = "fa-solid fa-credit-card"

class PaymentHistoryAdmin(ModelView, model=PaymentHistory):
    column_list = [c.key for c in inspect(PaymentHistory).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Payment History"
    name_plural = "Payment History"
    icon = "fa-solid fa-credit-card"

class ReferralAdmin(ModelView, model=Referral):
    column_list = [c.key for c in inspect(Referral).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Referral"
    name_plural = "Referrals"
    icon = "fa-solid fa-share"

class EloHistoryAdmin(ModelView, model=EloHistory):
    column_list = [c.key for c in inspect(EloHistory).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "ELO History"
    name_plural = "ELO History"
    icon = "fa-solid fa-chart-line"

class QuizQuestionAdmin(ModelView, model=QuizQuestion):
    column_list = [c.key for c in inspect(QuizQuestion).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Quiz Question"
    name_plural = "Quiz Questions"
    icon = "fa-solid fa-question"

class QuizSessionAdmin(ModelView, model=QuizSession):
    column_list = [c.key for c in inspect(QuizSession).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Quiz Session"
    name_plural = "Quiz Sessions"
    icon = "fa-solid fa-clipboard-list"

class SurveyAdmin(ModelView, model=Survey):
    column_list = [c.key for c in inspect(Survey).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Survey"
    name_plural = "Surveys"
    icon = "fa-solid fa-poll"

class UserAnswerAdmin(ModelView, model=UserAnswer):
    column_list = [c.key for c in inspect(UserAnswer).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "User Answer"
    name_plural = "User Answers"
    icon = "fa-solid fa-reply"

class OnboardingStateAdmin(ModelView, model=OnboardingState):
    column_list = [c.key for c in inspect(OnboardingState).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Onboarding State"
    name_plural = "Onboarding States"
    icon = "fa-solid fa-flag"

class UserOnboardingStateAdmin(ModelView, model=UserOnboardingState):
    column_list = [c.key for c in inspect(UserOnboardingState).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "User Onboarding State"
    name_plural = "User Onboarding States"
    icon = "fa-solid fa-user-check"

class ProgrammingChallengeAdmin(ModelView, model=ProgrammingChallenge):
    column_list = [c.key for c in inspect(ProgrammingChallenge).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Programming Challenge"
    name_plural = "Programming Challenges"
    icon = "fa-solid fa-code"

class ProgrammingSessionAdmin(ModelView, model=ProgrammingSession):
    column_list = [c.key for c in inspect(ProgrammingSession).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Programming Session"
    name_plural = "Programming Sessions"
    icon = "fa-solid fa-laptop-code"

class LearningPodAdmin(ModelView, model=LearningPod):
    column_list = [c.key for c in inspect(LearningPod).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Learning Pod"
    name_plural = "Learning Pods"
    icon = "fa-solid fa-users"

class LearningPodMemberAdmin(ModelView, model=LearningPodMember):
    column_list = [c.key for c in inspect(LearningPodMember).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Learning Pod Member"
    name_plural = "Learning Pod Members"
    icon = "fa-solid fa-user-plus"

class LessonCategoryAdmin(ModelView, model=LessonCategory):
    column_list = [c.key for c in inspect(LessonCategory).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Lesson Category"
    name_plural = "Lesson Categories"
    icon = "fa-solid fa-folder"

class LessonAdmin(ModelView, model=Lesson):
    column_list = [c.key for c in inspect(Lesson).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Lesson"
    name_plural = "Lessons"
    icon = "fa-solid fa-book"

class LessonContentAdmin(ModelView, model=LessonContent):
    column_list = [c.key for c in inspect(LessonContent).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Lesson Content"
    name_plural = "Lesson Contents"
    icon = "fa-solid fa-file-alt"

class UserLessonAdmin(ModelView, model=UserLesson):
    column_list = [c.key for c in inspect(UserLesson).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "User Lesson"
    name_plural = "User Lessons"
    icon = "fa-solid fa-user-graduate"

class UserLessonIssueAdmin(ModelView, model=UserLessonIssue):
    column_list = [c.key for c in inspect(UserLessonIssue).columns]
    can_create = True
    can_edit = True
    can_delete = True
    name = "User Lesson Issue"
    name_plural = "User Lesson Issues"
    icon = "fa-solid fa-exclamation-triangle"

# Function to setup admin interface
def setup_admin(app):
    # Create Admin instance with authentication
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable must be set for admin authentication")
    authentication_backend = AdminAuthentication(secret_key=secret_key)
    admin = Admin(
        app, 
        engine, 
        authentication_backend=authentication_backend,
        title="ModernAI Pro Admin",
        base_url="/admin"
    )
    
    # Add model views
    admin.add_view(UserAdmin)
    admin.add_view(WorkshopAdmin)
    admin.add_view(WorkshopPaymentHistoryAdmin)
    admin.add_view(PaymentHistoryAdmin)
    admin.add_view(ReferralAdmin)
    admin.add_view(EloHistoryAdmin)
    admin.add_view(QuizQuestionAdmin)
    admin.add_view(QuizSessionAdmin)
    admin.add_view(SurveyAdmin)
    admin.add_view(UserAnswerAdmin)
    admin.add_view(OnboardingStateAdmin)
    admin.add_view(UserOnboardingStateAdmin)
    admin.add_view(ProgrammingChallengeAdmin)
    admin.add_view(ProgrammingSessionAdmin)
    admin.add_view(LearningPodAdmin)
    admin.add_view(LearningPodMemberAdmin)
    admin.add_view(LessonCategoryAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(LessonContentAdmin)
    admin.add_view(UserLessonAdmin)
    admin.add_view(UserLessonIssueAdmin)
    
    return admin
