export const BASE_TITLE = "ModernAI Education";
export const APP_VERSION = "0.1.1";
const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8001";
export const LOGIN_REQUEST = BASE_URL + "/login";

const AUTH_BASE = BASE_URL + "/auth";
export const REGISTER_REQUEST = AUTH_BASE + "/register";
export const FORGOT_PASSWORD_REQUEST = AUTH_BASE + "/forgot-password";
export const RESET_PASSWORD_REQUEST = AUTH_BASE + "/reset-password";
export const VERIFY_EMAIL_REQUEST = AUTH_BASE + "/verify-email";
export const RESEND_VERIFICATION_REQUEST = AUTH_BASE + "/resend-verification";


const QUIZ_BASE = BASE_URL + "/quiz";
export const START_QUIZ     = QUIZ_BASE + "/start_quiz";
export const GET_QUESTION   = QUIZ_BASE + "/get_question";
export const SUBMIT_ANSWER  = QUIZ_BASE + "/submit_answer";

const SURVEY_BASE = BASE_URL + "/survey";
export const CREATE_SURVEY = SURVEY_BASE + "/create_survey";

const RECORDING_BASE = BASE_URL + "/recording";
export const GET_RECORDING        = RECORDING_BASE + "/";
export const RECORDING_PUBLIC_URL = RECORDING_BASE + "/public_url";

const BLOG_BASE = BASE_URL + "/blog";
export const GET_POST = (id) => `${BLOG_BASE}/posts/${id}/`;

export const surveyTypes = [
  { label: "Single Word", value: "single_word" },
  { label: "Single Sentence", value: "single_sentence" },
  { label: "Poll", value: "poll" },
  { label: "Quiz", value: "quiz" },
  { label: "Ranking", value: "ranking" },
];
