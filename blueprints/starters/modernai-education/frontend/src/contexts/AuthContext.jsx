import React, { createContext, useContext, useState, useEffect } from "react";
import { 
  LOGIN_REQUEST, 
  REGISTER_REQUEST, 
  FORGOT_PASSWORD_REQUEST, 
  RESET_PASSWORD_REQUEST,
  VERIFY_EMAIL_REQUEST,
  RESEND_VERIFICATION_REQUEST
} from "../Constants";
import axios from "axios";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    const accessToken = localStorage.getItem("access_token");
    return !!accessToken;
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const login = async (credentials) => {
    setLoading(true);
    setError(null); // Reset any existing errors

    try {
      const params = new URLSearchParams();
      params.append("username", credentials.username);
      params.append("password", credentials.password);

      const response = await axios.post(
        LOGIN_REQUEST,
        params.toString(), // URLSearchParams object automatically encodes the parameters
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );

      // Extract the access token from the response
      const { access_token, token_type, user } = response.data;


      if (access_token && token_type) {
        localStorage.setItem("user", user.username);
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("role", user.role);
        localStorage.setItem("first_name", user.first_name);
        localStorage.setItem("last_name", user.last_name);
        // You might want to store other user fields too
        localStorage.setItem("email", user.email);
        localStorage.setItem("subscription_tier", user.subscription_tier);
        setIsAuthenticated(true);
      }
       else {
        throw new Error("Login failed due to server response");
      }
    } catch (error) {
      let errorMessage =
        error.response?.data?.detail ||
        "Login failed: Invalid username or password";
      
      // Special handling for unverified email
      if (error.response?.status === 403 && 
          (error.response?.headers?.['x-error'] === "email_not_verified" || 
           error.response?.data?.detail?.includes("Email not verified"))) {
        errorMessage = "Email not verified. Please check your email for verification link.";
      }
      
      setError(errorMessage); // Set the error state to the error message
      console.error("Login request failed:", error);
      throw errorMessage; // Throw the error message for the Login component to catch
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setIsAuthenticated(false);
    console.log("Logout getting processed");
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    localStorage.removeItem("first_name");
    localStorage.removeItem("last_name");
    localStorage.removeItem("email");
    localStorage.removeItem("subscription_tier");
  };
  
  const register = async (userData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(
        REGISTER_REQUEST,
        userData,
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      
      return response.data;
    } catch (error) {
      let errorMessage = "Registration failed. Please try again.";
      
      // Handle error message from response
      if (error.response?.data?.detail) {
        // If detail is a string, use it directly
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } 
        // If detail is an object or array (validation errors), format it as a string
        else if (typeof error.response.data.detail === 'object') {
          if (Array.isArray(error.response.data.detail)) {
            // If it's an array of validation errors, take the first one
            const firstError = error.response.data.detail[0];
            errorMessage = firstError.msg || JSON.stringify(firstError);
          } else {
            // Otherwise convert the object to a string
            errorMessage = JSON.stringify(error.response.data.detail);
          }
        }
      }
      
      // Special handling for welcome code errors
      if (error.response?.status === 400 && 
          (error.response?.headers?.['x-error'] === "invalid_welcome_code" || 
           error.response?.data?.detail === "Invalid welcome code")) {
        errorMessage = "Invalid welcome code. Please check and try again.";
      }
      
      setError(errorMessage);
      throw errorMessage;
    } finally {
      setLoading(false);
    }
  };
  
  const forgotPassword = async (email) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(
        FORGOT_PASSWORD_REQUEST,
        { email },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      
      return response.data;
    } catch (error) {
      let errorMessage = "Failed to send password reset email. Please try again.";
      
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (typeof error.response.data.detail === 'object') {
          errorMessage = JSON.stringify(error.response.data.detail);
        }
      }
      
      setError(errorMessage);
      throw errorMessage;
    } finally {
      setLoading(false);
    }
  };
  
  const resetPassword = async (token, newPassword) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(
        RESET_PASSWORD_REQUEST,
        { token, new_password: newPassword },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      
      return response.data;
    } catch (error) {
      let errorMessage = "Failed to reset password. Token may be invalid or expired.";
      
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (typeof error.response.data.detail === 'object') {
          errorMessage = JSON.stringify(error.response.data.detail);
        }
      }
      
      setError(errorMessage);
      throw errorMessage;
    } finally {
      setLoading(false);
    }
  };

  const verifyEmail = async (token) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(
        VERIFY_EMAIL_REQUEST,
        { token },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      
      return response.data;
    } catch (error) {
      let errorMessage = "Failed to verify email. Token may be invalid or expired.";
      
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (typeof error.response.data.detail === 'object') {
          errorMessage = JSON.stringify(error.response.data.detail);
        }
      }
      
      setError(errorMessage);
      throw errorMessage;
    } finally {
      setLoading(false);
    }
  };
  
  const resendVerification = async (email) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(
        RESEND_VERIFICATION_REQUEST,
        { email },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      
      return response.data;
    } catch (error) {
      let errorMessage = "Failed to resend verification email.";
      
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (typeof error.response.data.detail === 'object') {
          errorMessage = JSON.stringify(error.response.data.detail);
        }
      }
      
      setError(errorMessage);
      throw errorMessage;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    isAuthenticated,
    loading,
    error,
    login,
    logout,
    register,
    forgotPassword,
    resetPassword,
    verifyEmail,
    resendVerification
  };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
export const useAuth = () => useContext(AuthContext);
