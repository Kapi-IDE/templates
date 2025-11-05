import React, { useEffect, useState } from "react";
import {
  useToast,
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Checkbox,
  Stack,
  Button,
  Heading,
  Text,
  Link,
  useColorModeValue,
  HStack,
  Center,
  FormErrorMessage,
  Alert,
  AlertIcon,
} from "@chakra-ui/react";
import Logo from "./Logo";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate, useSearchParams } from "react-router-dom";
import { BASE_TITLE } from "../Constants";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";

// Login view component
const LoginView = ({ onForgotPassword, onRegister, onSubmit, onVerify, loading, loginError }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(false);
  
  // Check if error is about unverified email
  const isUnverifiedEmailError = loginError && loginError.toLowerCase().includes("email not verified");
  
  const handleLogin = (e) => {
    e.preventDefault();
    onSubmit(username, password, remember);
  };
  
  return (
    <Stack spacing={6} as="form" onSubmit={handleLogin}>
      <FormControl id="username" isRequired>
        <FormLabel>Username</FormLabel>
        <Input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          size="lg"
          bg={useColorModeValue("white", "gray.700")}
        />
      </FormControl>
      
      <FormControl id="password" isRequired>
        <FormLabel>Password</FormLabel>
        <InputGroup size="lg">
          <Input
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            bg={useColorModeValue("white", "gray.700")}
          />
          <InputRightElement width="4.5rem">
            <Button
              h="1.75rem"
              size="sm"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <ViewOffIcon /> : <ViewIcon />}
            </Button>
          </InputRightElement>
        </InputGroup>
      </FormControl>
      
      <Stack direction="row" align="start" justify="space-between">
        <Checkbox isChecked={remember} onChange={(e) => setRemember(e.target.checked)}>
          Remember me
        </Checkbox>
        <Link color="purple.400" onClick={onForgotPassword}>
          Forgot password?
        </Link>
      </Stack>
      
      {isUnverifiedEmailError && (
        <Alert status="warning" rounded="md" mb={2}>
          <AlertIcon />
          <Box flex="1">
            <Text>Email not verified.</Text>
            <Button 
              variant="link" 
              colorScheme="purple" 
              size="sm" 
              onClick={onVerify}
              mt={1}
            >
              Resend verification email
            </Button>
          </Box>
        </Alert>
      )}
      
      <Button
        isLoading={loading}
        type="submit"
        bg="purple.500"
        color="white"
        size="lg"
        _hover={{
          bg: "purple.600",
        }}
        fontSize="md"
      >
        Sign in
      </Button>
      
      <Stack pt={6}>
        <Text align="center">
          Don't have an account?{" "}
          <Link color="purple.400" onClick={onRegister}>
            Register
          </Link>
        </Text>
      </Stack>
    </Stack>
  );
};

// Register view component
const RegisterView = ({ onLogin, onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    firstName: "",
    lastName: "",
    welcomeCode: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  
  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({
      ...formData,
      [id]: value,
    });
    
    // Clear error when field is edited
    if (formErrors[id]) {
      setFormErrors({
        ...formErrors,
        [id]: "",
      });
    }
  };
  
  const validateForm = () => {
    const errors = {};
    
    if (!formData.username.trim()) {
      errors.username = "Username is required";
    }
    
    if (!formData.email.trim()) {
      errors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = "Email is invalid";
    }
    
    if (!formData.password) {
      errors.password = "Password is required";
    } else if (formData.password.length < 8) {
      errors.password = "Password must be at least 8 characters";
    }
    
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = "Passwords do not match";
    }
    
    if (!formData.firstName.trim()) {
      errors.firstName = "First name is required";
    }
    
    if (!formData.lastName.trim()) {
      errors.lastName = "Last name is required";
    }
    
    if (!formData.welcomeCode.trim()) {
      errors.welcomeCode = "Welcome code is required";
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };
  
  const handleRegister = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        first_name: formData.firstName,
        last_name: formData.lastName,
        welcome_code: formData.welcomeCode,
      });
    }
  };
  
  return (
    <Stack spacing={4} as="form" onSubmit={handleRegister}>
      <HStack>
        <FormControl id="firstName" isRequired isInvalid={!!formErrors.firstName}>
          <FormLabel>First Name</FormLabel>
          <Input
            type="text"
            value={formData.firstName}
            onChange={handleChange}
            bg={useColorModeValue("white", "gray.700")}
          />
          <FormErrorMessage>{formErrors.firstName}</FormErrorMessage>
        </FormControl>
        
        <FormControl id="lastName" isRequired isInvalid={!!formErrors.lastName}>
          <FormLabel>Last Name</FormLabel>
          <Input
            type="text"
            value={formData.lastName}
            onChange={handleChange}
            bg={useColorModeValue("white", "gray.700")}
          />
          <FormErrorMessage>{formErrors.lastName}</FormErrorMessage>
        </FormControl>
      </HStack>
      
      <FormControl id="username" isRequired isInvalid={!!formErrors.username}>
        <FormLabel>Username</FormLabel>
        <Input
          type="text"
          value={formData.username}
          onChange={handleChange}
          bg={useColorModeValue("white", "gray.700")}
        />
        <FormErrorMessage>{formErrors.username}</FormErrorMessage>
      </FormControl>
      
      <FormControl id="email" isRequired isInvalid={!!formErrors.email}>
        <FormLabel>Email</FormLabel>
        <Input
          type="email"
          value={formData.email}
          onChange={handleChange}
          bg={useColorModeValue("white", "gray.700")}
        />
        <FormErrorMessage>{formErrors.email}</FormErrorMessage>
      </FormControl>
      
      <FormControl id="password" isRequired isInvalid={!!formErrors.password}>
        <FormLabel>Password</FormLabel>
        <InputGroup>
          <Input
            type={showPassword ? "text" : "password"}
            value={formData.password}
            onChange={handleChange}
            bg={useColorModeValue("white", "gray.700")}
          />
          <InputRightElement width="4.5rem">
            <Button
              h="1.75rem"
              size="sm"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <ViewOffIcon /> : <ViewIcon />}
            </Button>
          </InputRightElement>
        </InputGroup>
        <FormErrorMessage>{formErrors.password}</FormErrorMessage>
      </FormControl>
      
      <FormControl id="confirmPassword" isRequired isInvalid={!!formErrors.confirmPassword}>
        <FormLabel>Confirm Password</FormLabel>
        <Input
          type={showPassword ? "text" : "password"}
          value={formData.confirmPassword}
          onChange={handleChange}
          bg={useColorModeValue("white", "gray.700")}
        />
        <FormErrorMessage>{formErrors.confirmPassword}</FormErrorMessage>
      </FormControl>
      
      <FormControl id="welcomeCode" isRequired isInvalid={!!formErrors.welcomeCode}>
        <FormLabel>Welcome Code</FormLabel>
        <Input
          type="text"
          value={formData.welcomeCode}
          onChange={handleChange}
          bg={useColorModeValue("white", "gray.700")}
          placeholder="Enter the welcome code you received"
        />
        <FormErrorMessage>{formErrors.welcomeCode}</FormErrorMessage>
        <Text fontSize="xs" color={useColorModeValue("gray.600", "gray.400")} mt={1}>
          A welcome code is required to register. You should have received this code from your instructor or administrator.
        </Text>
      </FormControl>
      
      <Stack spacing={6} pt={4}>
        <Button
          isLoading={loading}
          type="submit"
          size="lg"
          bg="purple.500"
          color="white"
          _hover={{
            bg: "purple.600",
          }}
        >
          Create Account
        </Button>
        
        <Text align="center">
          Already have an account?{" "}
          <Link color="purple.400" onClick={onLogin}>
            Sign In
          </Link>
        </Text>
      </Stack>
    </Stack>
  );
};

// Forgot Password view component
const ForgotPasswordView = ({ onLogin, onSubmit, loading, success }) => {
  const [email, setEmail] = useState("");
  const [emailError, setEmailError] = useState("");
  
  const validateEmail = () => {
    if (!email.trim()) {
      setEmailError("Email is required");
      return false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      setEmailError("Email is invalid");
      return false;
    }
    setEmailError("");
    return true;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateEmail()) {
      onSubmit(email);
    }
  };
  
  return (
    <Stack spacing={4} as="form" onSubmit={handleSubmit}>
      {success && (
        <Alert status="success" rounded="md">
          <AlertIcon />
          Password reset link has been sent to your email.
        </Alert>
      )}
      
      <Text fontSize="sm" color={useColorModeValue("gray.600", "gray.400")}>
        Enter your email and we'll send you a link to reset your password.
      </Text>
      
      <FormControl id="email" isRequired isInvalid={!!emailError}>
        <FormLabel>Email</FormLabel>
        <Input
          type="email"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
            if (emailError) setEmailError("");
          }}
          bg={useColorModeValue("white", "gray.700")}
        />
        <FormErrorMessage>{emailError}</FormErrorMessage>
      </FormControl>
      
      <Stack spacing={6} pt={4}>
        <Button
          isLoading={loading}
          type="submit"
          size="lg"
          bg="purple.500"
          color="white"
          _hover={{
            bg: "purple.600",
          }}
        >
          Send Reset Link
        </Button>
        
        <Text align="center">
          Remember your password?{" "}
          <Link color="purple.400" onClick={onLogin}>
            Sign In
          </Link>
        </Text>
      </Stack>
    </Stack>
  );
};

// Email Verification view component
const EmailVerificationView = ({ token, onLogin, onSubmit, loading, success, onResendVerification }) => {
  const [email, setEmail] = useState("");
  const [emailError, setEmailError] = useState("");
  
  // Lift all color mode values to the top level to avoid conditional hook calls
  const textColor = useColorModeValue("gray.600", "gray.400");
  const inputBgColor = useColorModeValue("white", "gray.700");
  
  const validateEmail = () => {
    if (!email.trim()) {
      setEmailError("Email is required");
      return false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      setEmailError("Email is invalid");
      return false;
    }
    setEmailError("");
    return true;
  };
  
  const handleResend = (e) => {
    e.preventDefault();
    if (validateEmail()) {
      onResendVerification(email);
    }
  };
  
  return (
    <Stack spacing={4}>
      {token ? (
        <Stack spacing={4}>
          {success ? (
            <Alert status="success" rounded="md">
              <AlertIcon />
              Your email has been successfully verified!
            </Alert>
          ) : (
            <>
              <Text fontSize="sm" color={textColor}>
                Verifying your email...
              </Text>
              <Button
                isLoading={loading}
                onClick={() => onSubmit(token)}
                size="lg"
                bg="purple.500"
                color="white"
                _hover={{
                  bg: "purple.600",
                }}
              >
                Verify Email
              </Button>
            </>
          )}
          
          <Text align="center" mt={4}>
            <Link color="purple.400" onClick={onLogin}>
              Return to Login
            </Link>
          </Text>
        </Stack>
      ) : (
        <Stack spacing={4} as="form" onSubmit={handleResend}>
          <Text fontSize="sm" color={textColor}>
            Enter your email to receive a new verification link.
          </Text>
          
          <FormControl id="verifyEmail" isRequired isInvalid={!!emailError}>
            <FormLabel>Email</FormLabel>
            <Input
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (emailError) setEmailError("");
              }}
              bg={inputBgColor}
            />
            <FormErrorMessage>{emailError}</FormErrorMessage>
          </FormControl>
          
          <Button
            isLoading={loading}
            type="submit"
            size="lg"
            bg="purple.500"
            color="white"
            _hover={{
              bg: "purple.600",
            }}
          >
            Resend Verification Link
          </Button>
          
          <Text align="center">
            Remember your password?{" "}
            <Link color="purple.400" onClick={onLogin}>
              Sign In
            </Link>
          </Text>
        </Stack>
      )}
    </Stack>
  );
};

// Reset Password view component
const ResetPasswordView = ({ token, onLogin, onSubmit, loading, success }) => {
  const [formData, setFormData] = useState({
    password: "",
    confirmPassword: ""
  });
  const [showPassword, setShowPassword] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  
  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({
      ...formData,
      [id]: value,
    });
    
    // Clear error when field is edited
    if (formErrors[id]) {
      setFormErrors({
        ...formErrors,
        [id]: "",
      });
    }
  };
  
  const validateForm = () => {
    const errors = {};
    
    if (!formData.password) {
      errors.password = "Password is required";
    } else if (formData.password.length < 8) {
      errors.password = "Password must be at least 8 characters";
    }
    
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = "Passwords do not match";
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };
  
  const handleResetPassword = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(token, formData.password);
    }
  };
  
  return (
    <Stack spacing={4} as="form" onSubmit={handleResetPassword}>
      {success && (
        <Alert status="success" rounded="md">
          <AlertIcon />
          Your password has been successfully reset!
        </Alert>
      )}
      
      <FormControl id="password" isRequired isInvalid={!!formErrors.password}>
        <FormLabel>New Password</FormLabel>
        <InputGroup>
          <Input
            type={showPassword ? "text" : "password"}
            value={formData.password}
            onChange={handleChange}
            bg={useColorModeValue("white", "gray.700")}
          />
          <InputRightElement width="4.5rem">
            <Button
              h="1.75rem"
              size="sm"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <ViewOffIcon /> : <ViewIcon />}
            </Button>
          </InputRightElement>
        </InputGroup>
        <FormErrorMessage>{formErrors.password}</FormErrorMessage>
      </FormControl>
      
      <FormControl id="confirmPassword" isRequired isInvalid={!!formErrors.confirmPassword}>
        <FormLabel>Confirm New Password</FormLabel>
        <Input
          type={showPassword ? "text" : "password"}
          value={formData.confirmPassword}
          onChange={handleChange}
          bg={useColorModeValue("white", "gray.700")}
        />
        <FormErrorMessage>{formErrors.confirmPassword}</FormErrorMessage>
      </FormControl>
      
      <Stack spacing={6} pt={4}>
        <Button
          isLoading={loading}
          type="submit"
          size="lg"
          bg="purple.500"
          color="white"
          _hover={{
            bg: "purple.600",
          }}
        >
          Reset Password
        </Button>
        
        {success && (
          <Text align="center">
            <Link color="purple.400" onClick={onLogin}>
              Return to Login
            </Link>
          </Text>
        )}
      </Stack>
    </Stack>
  );
};

// Main Login component that manages the different views
const Login = () => {
  useEffect(() => {
    document.title = `Login | ${BASE_TITLE}`;
  }, []);

  // Get tokens from URL query params
  const [searchParams] = useSearchParams();
  const resetToken = searchParams.get("token");
  const verifyToken = searchParams.get("verify");
  
  // Determine initial view based on tokens
  const getInitialView = () => {
    if (verifyToken) return "verifyEmail";
    if (resetToken) return "resetPassword";
    return "login";
  };
  
  // States
  const [view, setView] = useState(getInitialView());
  const [successMessage, setSuccessMessage] = useState("");
  const [loginErrorMessage, setLoginErrorMessage] = useState("");
  
  // Context hooks
  const toast = useToast();
  const { login, register, forgotPassword, resetPassword, verifyEmail, resendVerification, loading } = useAuth();
  const navigate = useNavigate();
  
  // Handle login submission
  const handleLogin = async (username, password, remember) => {
    setLoginErrorMessage("");
    try {
      await login({ username, password });
      toast({
        title: "Login successful",
        description: "Welcome!",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
      navigate("/");
    } catch (error) {
      setLoginErrorMessage(error || "An error occurred during login");
      toast({
        title: "Login failed",
        description: error || "An error occurred during login",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };
  
  // Handle registration submission
  const handleRegister = async (userData) => {
    try {
      await register(userData);
      toast({
        title: "Registration successful",
        description: "You can now log in with your new account.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
      setView("login");
    } catch (error) {
      toast({
        title: "Registration failed",
        description: error || "An error occurred during registration",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };
  
  // Handle forgot password submission
  const handleForgotPassword = async (email) => {
    try {
      await forgotPassword(email);
      setSuccessMessage("Password reset link has been sent to your email.");
    } catch (error) {
      toast({
        title: "Failed to send reset link",
        description: error || "Please try again later",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };
  
  // Handle reset password submission
  const handleResetPassword = async (token, newPassword) => {
    try {
      await resetPassword(token, newPassword);
      setSuccessMessage("Your password has been successfully reset!");
    } catch (error) {
      toast({
        title: "Failed to reset password",
        description: error || "Token may be invalid or expired",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };
  
  // Handle email verification
  const handleVerifyEmail = async (token) => {
    try {
      await verifyEmail(token);
      setSuccessMessage("Your email has been successfully verified!");
      toast({
        title: "Email verified",
        description: "Your email has been successfully verified. You can now log in.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "Failed to verify email",
        description: error || "Token may be invalid or expired",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };
  
  // Handle resend verification email
  const handleResendVerification = async (email) => {
    try {
      await resendVerification(email);
      toast({
        title: "Verification email sent",
        description: "If your email is registered, you will receive a new verification link.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "Failed to send verification email",
        description: error || "Please try again later",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Flex
      minH="100vh"
      justify="center"
      align="center"
      bgImage={`url(/images/robot_background.jpg)`}
      bgSize="cover"
      bgPosition="center"
      position="relative"
    >
      {/* Semi-transparent overlay to improve text readability */}
      <Box
        position="absolute"
        top="0"
        left="0"
        right="0"
        bottom="0"
        bg="blackAlpha.600"
        zIndex="1"
      />
      
      <Stack 
        spacing={8} 
        mx="auto" 
        maxW="lg" 
        py={12} 
        px={6} 
        zIndex="2"
        position="relative"
        width="100%"
      >
        <Stack align="center" spacing={3}>
          <Logo fontSize="240px" color="white" />
          <Heading fontSize="3xl" color="white">
            {view === "login" && "Sign in to your account"}
            {view === "register" && "Create an account"}
            {view === "forgotPassword" && "Forgot Password"}
            {view === "resetPassword" && "Reset Your Password"}
            {view === "verifyEmail" && "Verify Your Email"}
          </Heading>
          {view === "login" && (
            <Text fontSize="lg" color="gray.200">
              Get ready to accelerate your AI career
            </Text>
          )}
        </Stack>
        
        <Box
          rounded="xl"
          bg={useColorModeValue("white", "gray.800")}
          boxShadow="2xl"
          p={8}
          width="100%"
          borderWidth="1px"
          borderColor="purple.400"
        >
          {view === "login" && (
            <LoginView
              onForgotPassword={() => setView("forgotPassword")}
              onRegister={() => setView("register")}
              onVerify={() => setView("verifyEmail")}
              onSubmit={handleLogin}
              loading={loading}
              loginError={loginErrorMessage}
            />
          )}
          
          {view === "register" && (
            <RegisterView
              onLogin={() => setView("login")}
              onSubmit={handleRegister}
              loading={loading}
            />
          )}
          
          {view === "forgotPassword" && (
            <ForgotPasswordView
              onLogin={() => setView("login")}
              onSubmit={handleForgotPassword}
              loading={loading}
              success={!!successMessage}
            />
          )}
          
          {view === "resetPassword" && (
            <ResetPasswordView
              token={resetToken}
              onLogin={() => setView("login")}
              onSubmit={handleResetPassword}
              loading={loading}
              success={!!successMessage}
            />
          )}
          
          {view === "verifyEmail" && (
            <EmailVerificationView
              token={verifyToken}
              onLogin={() => setView("login")}
              onSubmit={handleVerifyEmail}
              onResendVerification={handleResendVerification}
              loading={loading}
              success={!!successMessage}
            />
          )}
        </Box>
      </Stack>
    </Flex>
  );
};

export default Login;