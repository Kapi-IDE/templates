/**
 * Healthcare AI Triage System - End-to-End Test Configuration
 * 
 * Comprehensive E2E testing with Playwright covering:
 * - Complete user workflows (patient registration to discharge)
 * - Cross-browser compatibility (Chrome, Firefox, Safari)
 * - Mobile responsive testing
 * - Accessibility compliance (WCAG 2.1 AA)
 * - Performance benchmarks
 * - Security testing
 * - HIPAA compliance validation
 */

import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config({ path: '.env.test' });

/**
 * See https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests',
  
  /* Maximum time one test can run for */
  timeout: 30 * 1000,
  
  /* Test timeout for expect() calls */
  expect: {
    /* Maximum time expect() should wait for the condition to be met */
    timeout: 5000,
    
    /* Threshold for screenshot comparisons */
    threshold: 0.2,
    
    /* Mode for screenshot comparisons */
    mode: 'strict'
  },

  /* Run tests in files in parallel */
  fullyParallel: true,
  
  /* Fail the build on CI if you accidentally left test.only in the source code */
  forbidOnly: !!process.env.CI,
  
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  
  /* Opt out of parallel tests on CI */
  workers: process.env.CI ? 1 : undefined,

  /* Reporter to use */
  reporter: [
    ['html', { outputFolder: 'test-results/html-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['line'],
    ['allure-playwright', { outputFolder: 'test-results/allure-results' }]
  ],

  /* Shared settings for all the projects below */
  use: {
    /* Base URL to use in actions like `await page.goto('/')` */
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
    
    /* Collect trace when retrying the failed test */
    trace: 'on-first-retry',
    
    /* Record video only on failure */
    video: 'retain-on-failure',
    
    /* Take screenshot only on failure */
    screenshot: 'only-on-failure',
    
    /* Ignore HTTPS errors for local testing */
    ignoreHTTPSErrors: process.env.NODE_ENV === 'development',
    
    /* Global test timeout */
    actionTimeout: 10000,
    
    /* Navigation timeout */
    navigationTimeout: 15000,
    
    /* Default user agent */
    userAgent: 'HealthcareTriageE2E/1.0',
    
    /* Viewport settings */
    viewport: { width: 1280, height: 720 },
    
    /* Locale and timezone */
    locale: 'en-US',
    timezoneId: 'America/New_York',
    
    /* Color scheme */
    colorScheme: 'light',
    
    /* Extra HTTP headers */
    extraHTTPHeaders: {
      'X-Test-Environment': 'e2e',
      'X-HIPAA-Audit-Token': 'test-audit-token'
    }
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
      teardown: 'cleanup'
    },
    {
      name: 'cleanup',
      testMatch: /.*\.teardown\.ts/
    },

    /* Desktop browsers */
    {
      name: 'chromium-desktop',
      use: { 
        ...devices['Desktop Chrome'],
        launchOptions: {
          args: [
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-dev-shm-usage',
            '--no-sandbox'
          ]
        }
      },
      dependencies: ['setup']
    },

    {
      name: 'firefox-desktop',
      use: { 
        ...devices['Desktop Firefox'],
        launchOptions: {
          firefoxUserPrefs: {
            'network.http.spdy.enabled': false,
            'network.http.http2.enabled': false
          }
        }
      },
      dependencies: ['setup']
    },

    {
      name: 'webkit-desktop',
      use: { 
        ...devices['Desktop Safari']
      },
      dependencies: ['setup']
    },

    /* Mobile devices */
    {
      name: 'mobile-chrome',
      use: { 
        ...devices['Pixel 5']
      },
      dependencies: ['setup']
    },

    {
      name: 'mobile-safari',
      use: { 
        ...devices['iPhone 12']
      },
      dependencies: ['setup']
    },

    /* Tablet devices */
    {
      name: 'tablet-chrome',
      use: { 
        ...devices['iPad Pro'],
        userAgent: devices['iPad Pro'].userAgent?.replace('Safari', 'Chrome') || ''
      },
      dependencies: ['setup']
    },

    /* Accessibility testing */
    {
      name: 'accessibility',
      use: { 
        ...devices['Desktop Chrome'],
        reducedMotion: 'reduce'
      },
      testMatch: /.*\.accessibility\.spec\.ts/,
      dependencies: ['setup']
    },

    /* Performance testing */
    {
      name: 'performance',
      use: { 
        ...devices['Desktop Chrome'],
        launchOptions: {
          args: ['--enable-precise-memory-info']
        }
      },
      testMatch: /.*\.performance\.spec\.ts/,
      dependencies: ['setup']
    },

    /* Security testing */
    {
      name: 'security',
      use: { 
        ...devices['Desktop Chrome']
      },
      testMatch: /.*\.security\.spec\.ts/,
      dependencies: ['setup']
    },

    /* Visual regression testing */
    {
      name: 'visual',
      use: { 
        ...devices['Desktop Chrome']
      },
      testMatch: /.*\.visual\.spec\.ts/,
      dependencies: ['setup']
    }
  ],

  /* Global setup and teardown */
  globalSetup: require.resolve('./global-setup'),
  globalTeardown: require.resolve('./global-teardown'),

  /* Test configuration */
  testConfig: {
    /* Test data directory */
    testDataDir: './test-data',
    
    /* Screenshots directory */
    screenshotDir: './test-results/screenshots',
    
    /* Video directory */
    videoDir: './test-results/videos',
    
    /* Trace directory */
    traceDir: './test-results/traces'
  },

  /* Healthcare-specific configuration */
  healthcare: {
    /* HIPAA compliance testing */
    hipaaCompliance: {
      enabled: true,
      auditLogging: true,
      dataEncryption: true,
      accessControl: true
    },
    
    /* Clinical accuracy testing */
    clinicalAccuracy: {
      enabled: true,
      triageScenarios: './test-data/clinical-scenarios.json',
      expectedOutcomes: './test-data/expected-outcomes.json',
      toleranceLevel: 0.1
    },
    
    /* Performance benchmarks */
    performance: {
      pageLoad: 3000,      // 3 seconds max
      apiResponse: 2000,   // 2 seconds max
      triageAssessment: 5000, // 5 seconds max
      searchQuery: 1000    // 1 second max
    },
    
    /* Security testing */
    security: {
      xssProtection: true,
      sqlInjection: true,
      csrfProtection: true,
      sessionSecurity: true,
      dataValidation: true
    }
  },

  /* Retry configuration */
  retryConfig: {
    /* Retry failed tests */
    retries: process.env.CI ? 3 : 1,
    
    /* Retry timeout */
    retryTimeout: 60000,
    
    /* Conditions for retry */
    retryConditions: [
      'timeout',
      'networkError',
      'browserCrash'
    ]
  },

  /* Parallelization */
  parallelConfig: {
    /* Number of parallel workers */
    workers: process.env.CI ? 2 : 4,
    
    /* Shard configuration for CI */
    shard: process.env.CI ? {
      total: parseInt(process.env.TOTAL_SHARDS || '1'),
      current: parseInt(process.env.SHARD_INDEX || '1')
    } : undefined
  },

  /* Environment-specific overrides */
  ...(process.env.NODE_ENV === 'production' && {
    use: {
      baseURL: process.env.PRODUCTION_URL,
      ignoreHTTPSErrors: false
    }
  }),

  ...(process.env.NODE_ENV === 'staging' && {
    use: {
      baseURL: process.env.STAGING_URL,
      ignoreHTTPSErrors: false
    }
  }),

  /* Web server configuration for local testing */
  webServer: process.env.CI ? undefined : {
    command: 'npm run start:test',
    port: 3000,
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
    env: {
      NODE_ENV: 'test',
      PORT: '3000'
    }
  },

  /* Metadata */
  metadata: {
    testSuite: 'Healthcare AI Triage System E2E Tests',
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    browser: 'multi-browser',
    platform: process.platform,
    author: 'KAPI Healthcare Solutions'
  }
});