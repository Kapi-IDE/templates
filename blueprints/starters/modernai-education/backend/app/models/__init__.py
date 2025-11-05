from app.database import Base

# Import models in dependency order
from app.models.quiz import QuizSession, QuizQuestion, UserAnswer, Survey
from app.models.onboarding import OnboardingState, UserOnboardingState
from app.models.programming import ProgrammingChallenge, ProgrammingSession, LearningPod, LearningPodMember
from app.models.learning import LessonCategory, Lesson, LessonContent, UserLesson, UserLessonIssue
from app.models.user import User, UserRoles, SubscriptionTier, PaymentHistory, Referral, EloHistory
from app.models.workshop import Workshop, WorkshopPaymentHistory

# Make all models available from the models package
__all__ = [
    "Base",
    "QuizSession", "QuizQuestion", "UserAnswer", "Survey",
    "OnboardingState", "UserOnboardingState",
    "ProgrammingChallenge", "ProgrammingSession", "LearningPod", "LearningPodMember",
    "LessonCategory", "Lesson", "LessonContent", "UserLesson", "UserLessonIssue",
    "User", "UserRoles", "SubscriptionTier", "PaymentHistory", "Referral", "EloHistory",
    "Workshop", "WorkshopPaymentHistory"
]