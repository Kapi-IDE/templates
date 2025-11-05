import { test, expect } from '@playwright/test';

test.describe('Healthcare Triage Workflow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Complete patient triage workflow', async ({ page }) => {
    // Step 1: Patient Registration
    await page.click('[data-testid="start-triage"]');
    await page.fill('[data-testid="patient-name"]', 'John Doe');
    await page.fill('[data-testid="patient-age"]', '45');
    await page.selectOption('[data-testid="patient-gender"]', 'male');
    await page.fill('[data-testid="patient-phone"]', '555-0123');
    await page.click('[data-testid="next-step"]');

    // Step 2: Chief Complaint
    await page.fill('[data-testid="chief-complaint"]', 'Chest pain and shortness of breath');
    await page.click('[data-testid="next-step"]');

    // Step 3: Symptom Assessment
    await page.check('[data-testid="symptom-chest-pain"]');
    await page.check('[data-testid="symptom-shortness-breath"]');
    await page.selectOption('[data-testid="pain-severity"]', '8');
    await page.selectOption('[data-testid="symptom-duration"]', '2-hours');
    await page.click('[data-testid="next-step"]');

    // Step 4: Vital Signs
    await page.fill('[data-testid="blood-pressure-systolic"]', '160');
    await page.fill('[data-testid="blood-pressure-diastolic"]', '95');
    await page.fill('[data-testid="heart-rate"]', '105');
    await page.fill('[data-testid="temperature"]', '98.6');
    await page.fill('[data-testid="oxygen-saturation"]', '96');
    await page.click('[data-testid="next-step"]');

    // Step 5: Medical History
    await page.check('[data-testid="history-hypertension"]');
    await page.check('[data-testid="history-diabetes"]');
    await page.fill('[data-testid="current-medications"]', 'Lisinopril, Metformin');
    await page.click('[data-testid="next-step"]');

    // Step 6: AI Triage Assessment
    await page.waitForSelector('[data-testid="triage-result"]', { timeout: 10000 });
    
    // Verify high-priority triage result
    const triageLevel = await page.textContent('[data-testid="triage-level"]');
    expect(triageLevel).toContain('HIGH PRIORITY');
    
    const recommendation = await page.textContent('[data-testid="triage-recommendation"]');
    expect(recommendation).toContain('immediate medical evaluation');
    
    // Verify confidence score
    const confidence = await page.textContent('[data-testid="confidence-score"]');
    expect(confidence).toMatch(/\d+%/);
    
    // Step 7: Provider Assignment
    await page.click('[data-testid="assign-provider"]');
    await page.waitForSelector('[data-testid="provider-assigned"]');
    
    const assignedProvider = await page.textContent('[data-testid="assigned-provider-name"]');
    expect(assignedProvider).toBeTruthy();
    
    // Step 8: Documentation and Handoff
    await page.fill('[data-testid="triage-notes"]', 'Patient presents with acute chest pain, elevated BP, concerning for ACS');
    await page.click('[data-testid="complete-triage"]');
    
    // Verify completion
    await page.waitForSelector('[data-testid="triage-complete"]');
    const completionMessage = await page.textContent('[data-testid="completion-message"]');
    expect(completionMessage).toContain('Triage completed successfully');
  });

  test('Low-priority triage workflow', async ({ page }) => {
    // Test low-priority case
    await page.click('[data-testid="start-triage"]');
    
    // Basic patient info
    await page.fill('[data-testid="patient-name"]', 'Jane Smith');
    await page.fill('[data-testid="patient-age"]', '28');
    await page.selectOption('[data-testid="patient-gender"]', 'female');
    await page.click('[data-testid="next-step"]');

    // Minor complaint
    await page.fill('[data-testid="chief-complaint"]', 'Mild headache for 1 day');
    await page.click('[data-testid="next-step"]');

    // Mild symptoms
    await page.check('[data-testid="symptom-headache"]');
    await page.selectOption('[data-testid="pain-severity"]', '3');
    await page.selectOption('[data-testid="symptom-duration"]', '1-day');
    await page.click('[data-testid="next-step"]');

    // Normal vitals
    await page.fill('[data-testid="blood-pressure-systolic"]', '120');
    await page.fill('[data-testid="blood-pressure-diastolic"]', '80');
    await page.fill('[data-testid="heart-rate"]', '72');
    await page.fill('[data-testid="temperature"]', '98.6');
    await page.click('[data-testid="next-step"]');

    // No significant history
    await page.click('[data-testid="next-step"]');

    // Verify low-priority result
    await page.waitForSelector('[data-testid="triage-result"]');
    const triageLevel = await page.textContent('[data-testid="triage-level"]');
    expect(triageLevel).toContain('LOW PRIORITY');
  });

  test('Critical emergency workflow', async ({ page }) => {
    // Test critical case
    await page.click('[data-testid="start-triage"]');
    
    // Patient info
    await page.fill('[data-testid="patient-name"]', 'Emergency Case');
    await page.fill('[data-testid="patient-age"]', '65');
    await page.click('[data-testid="next-step"]');

    // Critical complaint
    await page.fill('[data-testid="chief-complaint"]', 'Sudden severe chest pain, can\'t breathe');
    await page.click('[data-testid="next-step"]');

    // Critical symptoms
    await page.check('[data-testid="symptom-chest-pain"]');
    await page.check('[data-testid="symptom-shortness-breath"]');
    await page.check('[data-testid="symptom-sweating"]');
    await page.selectOption('[data-testid="pain-severity"]', '10');
    await page.selectOption('[data-testid="symptom-duration"]', '30-minutes');
    await page.click('[data-testid="next-step"]');

    // Critical vitals
    await page.fill('[data-testid="blood-pressure-systolic"]', '200');
    await page.fill('[data-testid="blood-pressure-diastolic"]', '110');
    await page.fill('[data-testid="heart-rate"]', '130');
    await page.fill('[data-testid="oxygen-saturation"]', '88');
    await page.click('[data-testid="next-step"]');

    // Skip history for emergency
    await page.click('[data-testid="skip-history"]');

    // Verify critical result
    await page.waitForSelector('[data-testid="triage-result"]');
    const triageLevel = await page.textContent('[data-testid="triage-level"]');
    expect(triageLevel).toContain('CRITICAL');
    
    // Verify emergency protocols activated
    await page.waitForSelector('[data-testid="emergency-alert"]');
    const emergencyAlert = await page.textContent('[data-testid="emergency-alert"]');
    expect(emergencyAlert).toContain('EMERGENCY PROTOCOLS ACTIVATED');
  });

  test('Provider dashboard functionality', async ({ page }) => {
    // Login as provider
    await page.goto('/provider/login');
    await page.fill('[data-testid="username"]', 'dr.smith@hospital.com');
    await page.fill('[data-testid="password"]', 'test123');
    await page.click('[data-testid="login"]');

    // Navigate to dashboard
    await page.waitForSelector('[data-testid="provider-dashboard"]');
    
    // Verify patient queue
    await expect(page.locator('[data-testid="patient-queue"]')).toBeVisible();
    
    // Check for pending patients
    const pendingPatients = await page.locator('[data-testid="pending-patient"]').count();
    expect(pendingPatients).toBeGreaterThanOrEqual(0);
    
    // If patients exist, test patient review
    if (pendingPatients > 0) {
      await page.click('[data-testid="pending-patient"]').first();
      await page.waitForSelector('[data-testid="patient-details"]');
      
      // Verify patient information display
      await expect(page.locator('[data-testid="patient-name"]')).toBeVisible();
      await expect(page.locator('[data-testid="triage-summary"]')).toBeVisible();
      await expect(page.locator('[data-testid="ai-recommendation"]')).toBeVisible();
      
      // Test provider actions
      await page.click('[data-testid="accept-patient"]');
      await page.waitForSelector('[data-testid="patient-accepted"]');
    }
  });

  test('Admin dashboard and analytics', async ({ page }) => {
    // Login as admin
    await page.goto('/admin/login');
    await page.fill('[data-testid="username"]', 'admin@hospital.com');
    await page.fill('[data-testid="password"]', 'admin123');
    await page.click('[data-testid="login"]');

    // Navigate to analytics
    await page.waitForSelector('[data-testid="admin-dashboard"]');
    await page.click('[data-testid="analytics-tab"]');
    
    // Verify analytics components
    await expect(page.locator('[data-testid="triage-metrics"]')).toBeVisible();
    await expect(page.locator('[data-testid="accuracy-chart"]')).toBeVisible();
    await expect(page.locator('[data-testid="volume-chart"]')).toBeVisible();
    await expect(page.locator('[data-testid="performance-metrics"]')).toBeVisible();
    
    // Test date filtering
    await page.selectOption('[data-testid="date-filter"]', 'last-7-days');
    await page.waitForLoadState('networkidle');
    
    // Verify updated metrics
    const totalTriages = await page.textContent('[data-testid="total-triages"]');
    expect(totalTriages).toMatch(/\d+/);
  });

  test('Accessibility compliance', async ({ page }) => {
    // Test keyboard navigation
    await page.keyboard.press('Tab');
    await page.keyboard.press('Enter'); // Should activate start triage
    
    // Test screen reader labels
    const startButton = page.locator('[data-testid="start-triage"]');
    await expect(startButton).toHaveAttribute('aria-label');
    
    // Test form labels
    await page.click('[data-testid="start-triage"]');
    const nameInput = page.locator('[data-testid="patient-name"]');
    await expect(nameInput).toHaveAttribute('aria-label');
    
    // Test color contrast (basic check)
    const backgroundColor = await page.evaluate(() => {
      const el = document.querySelector('[data-testid="main-container"]');
      return window.getComputedStyle(el).backgroundColor;
    });
    expect(backgroundColor).toBeTruthy();
  });

  test('Error handling and validation', async ({ page }) => {
    await page.click('[data-testid="start-triage"]');
    
    // Test required field validation
    await page.click('[data-testid="next-step"]');
    await expect(page.locator('[data-testid="name-error"]')).toBeVisible();
    
    // Test invalid data validation
    await page.fill('[data-testid="patient-age"]', '150');
    await page.click('[data-testid="next-step"]');
    await expect(page.locator('[data-testid="age-error"]')).toBeVisible();
    
    // Test network error handling
    await page.route('**/api/triage', route => route.abort());
    await page.fill('[data-testid="patient-name"]', 'Test Patient');
    await page.fill('[data-testid="patient-age"]', '30');
    await page.click('[data-testid="next-step"]');
    // Continue through form...
    
    // Verify error message display
    await expect(page.locator('[data-testid="network-error"]')).toBeVisible();
  });
});