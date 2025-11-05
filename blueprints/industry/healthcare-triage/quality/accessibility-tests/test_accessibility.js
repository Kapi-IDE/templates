/**
 * Accessibility testing for Healthcare Triage System
 * Tests WCAG 2.1 AA compliance and accessibility best practices
 */

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright');

class AccessibilityTestSuite {
  
  static async runAxeTests(page, context = 'page') {
    /**
     * Run axe-core accessibility tests
     */
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    // Log violations for debugging
    if (accessibilityScanResults.violations.length > 0) {
      console.log(`Accessibility violations found in ${context}:`);
      accessibilityScanResults.violations.forEach(violation => {
        console.log(`- ${violation.id}: ${violation.description}`);
        console.log(`  Impact: ${violation.impact}`);
        console.log(`  Help: ${violation.helpUrl}`);
      });
    }

    expect(accessibilityScanResults.violations).toEqual([]);
    return accessibilityScanResults;
  }

  static async testKeyboardNavigation(page) {
    /**
     * Test keyboard navigation throughout the application
     */
    
    // Start from the beginning
    await page.goto('/');
    
    // Test tab navigation through main interface
    const focusableElements = [
      '[data-testid="start-triage"]',
      '[data-testid="provider-login"]',
      '[data-testid="admin-login"]',
      '[data-testid="help-link"]'
    ];

    for (let i = 0; i < focusableElements.length; i++) {
      await page.keyboard.press('Tab');
      
      // Check if correct element is focused
      const focusedElement = await page.locator(':focus');
      const expectedElement = page.locator(focusableElements[i]);
      
      // Verify focus is on expected element
      await expect(focusedElement).toHaveAttribute('data-testid', 
        focusableElements[i].replace('[data-testid="', '').replace('"]', ''));
    }

    // Test Enter key activation
    await page.keyboard.press('Enter');
    await page.waitForSelector('[data-testid="patient-form"]');
    
    // Test form navigation
    const formElements = [
      '[data-testid="patient-name"]',
      '[data-testid="patient-age"]',
      '[data-testid="patient-gender"]',
      '[data-testid="patient-phone"]',
      '[data-testid="next-step"]'
    ];

    for (const element of formElements) {
      await page.keyboard.press('Tab');
      const focused = await page.locator(':focus');
      await expect(focused).toHaveAttribute('data-testid', 
        element.replace('[data-testid="', '').replace('"]', ''));
    }
  }

  static async testScreenReaderSupport(page) {
    /**
     * Test screen reader support and ARIA attributes
     */
    
    await page.goto('/');
    
    // Check main landmarks
    const landmarks = [
      { selector: 'main', role: 'main' },
      { selector: 'nav', role: 'navigation' },
      { selector: 'header', role: 'banner' },
      { selector: 'footer', role: 'contentinfo' }
    ];

    for (const landmark of landmarks) {
      const element = page.locator(landmark.selector);
      await expect(element).toHaveAttribute('role', landmark.role);
    }

    // Check heading hierarchy
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
    let previousLevel = 0;
    
    for (const heading of headings) {
      const tagName = await heading.evaluate(el => el.tagName.toLowerCase());
      const currentLevel = parseInt(tagName.charAt(1));
      
      // Heading levels should not skip (e.g., h1 to h3)
      expect(currentLevel - previousLevel).toBeLessThanOrEqual(1);
      previousLevel = currentLevel;
    }

    // Check ARIA labels and descriptions
    const interactiveElements = await page.locator('button, input, select, textarea, a').all();
    
    for (const element of interactiveElements) {
      const hasLabel = await element.evaluate(el => {
        return el.hasAttribute('aria-label') || 
               el.hasAttribute('aria-labelledby') ||
               el.labels?.length > 0 ||
               el.textContent?.trim().length > 0;
      });
      
      expect(hasLabel).toBe(true);
    }
  }

  static async testColorContrastAndVisualDesign(page) {
    /**
     * Test color contrast ratios and visual accessibility
     */
    
    await page.goto('/');
    
    // Test color contrast for text elements
    const textElements = await page.locator('p, span, div, button, a').all();
    
    for (const element of textElements) {
      const styles = await element.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return {
          color: computed.color,
          backgroundColor: computed.backgroundColor,
          fontSize: computed.fontSize
        };
      });
      
      // Basic check that colors are defined
      expect(styles.color).toBeTruthy();
      expect(styles.backgroundColor).toBeTruthy();
      
      // Font size should be at least 14px for accessibility
      const fontSize = parseInt(styles.fontSize);
      expect(fontSize).toBeGreaterThanOrEqual(14);
    }

    // Test focus indicators
    const focusableElements = await page.locator('button, input, select, textarea, a').all();
    
    for (const element of focusableElements) {
      await element.focus();
      
      const focusStyles = await element.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return {
          outline: computed.outline,
          outlineWidth: computed.outlineWidth,
          outlineColor: computed.outlineColor,
          boxShadow: computed.boxShadow
        };
      });
      
      // Should have visible focus indicator
      const hasFocusIndicator = focusStyles.outline !== 'none' || 
                               focusStyles.outlineWidth !== '0px' ||
                               focusStyles.boxShadow !== 'none';
      expect(hasFocusIndicator).toBe(true);
    }
  }

  static async testMobileAccessibility(page) {
    /**
     * Test accessibility on mobile devices
     */
    
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Test touch targets (should be at least 44px)
    const touchTargets = await page.locator('button, a, input, select').all();
    
    for (const target of touchTargets) {
      const box = await target.boundingBox();
      if (box) {
        expect(box.width).toBeGreaterThanOrEqual(44);
        expect(box.height).toBeGreaterThanOrEqual(44);
      }
    }

    // Test responsive design doesn't break accessibility
    await AccessibilityTestSuite.runAxeTests(page, 'mobile view');
    
    // Test horizontal scroll (shouldn't exist)
    const hasHorizontalScroll = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(hasHorizontalScroll).toBe(false);
  }

  static async testFormAccessibility(page) {
    /**
     * Test form accessibility features
     */
    
    await page.goto('/');
    await page.click('[data-testid="start-triage"]');
    
    // Test form labels and associations
    const formInputs = await page.locator('input, select, textarea').all();
    
    for (const input of formInputs) {
      const hasProperLabel = await input.evaluate(el => {
        // Check for explicit label association
        if (el.labels && el.labels.length > 0) return true;
        
        // Check for aria-label
        if (el.hasAttribute('aria-label')) return true;
        
        // Check for aria-labelledby
        if (el.hasAttribute('aria-labelledby')) {
          const labelId = el.getAttribute('aria-labelledby');
          return document.getElementById(labelId) !== null;
        }
        
        return false;
      });
      
      expect(hasProperLabel).toBe(true);
    }

    // Test error messages and validation
    await page.click('[data-testid="next-step"]'); // Submit without filling required fields
    
    const errorMessages = await page.locator('[role="alert"], .error-message').all();
    
    for (const errorMessage of errorMessages) {
      // Error messages should be associated with form fields
      const hasAriaDescribedBy = await errorMessage.evaluate(el => {
        const id = el.id;
        if (!id) return false;
        
        // Find form field that references this error
        const field = document.querySelector(`[aria-describedby*="${id}"]`);
        return field !== null;
      });
      
      expect(hasAriaDescribedBy).toBe(true);
    }

    // Test required field indicators
    const requiredFields = await page.locator('[required], [aria-required="true"]').all();
    
    for (const field of requiredFields) {
      const hasRequiredIndicator = await field.evaluate(el => {
        // Check for visual indicator (asterisk, etc.)
        const label = el.labels?.[0] || document.querySelector(`label[for="${el.id}"]`);
        if (label) {
          return label.textContent.includes('*') || 
                 label.textContent.includes('required') ||
                 label.querySelector('.required-indicator') !== null;
        }
        
        // Check aria-required
        return el.hasAttribute('aria-required') && el.getAttribute('aria-required') === 'true';
      });
      
      expect(hasRequiredIndicator).toBe(true);
    }
  }
}

// Test Suite Implementation
test.describe('Healthcare Triage Accessibility Tests', () => {
  
  test('WCAG 2.1 AA compliance - Main page', async ({ page }) => {
    await page.goto('/');
    await AccessibilityTestSuite.runAxeTests(page, 'main page');
  });

  test('WCAG 2.1 AA compliance - Triage form', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="start-triage"]');
    await AccessibilityTestSuite.runAxeTests(page, 'triage form');
  });

  test('WCAG 2.1 AA compliance - Provider dashboard', async ({ page }) => {
    // Login as provider first
    await page.goto('/provider/login');
    await page.fill('[data-testid="username"]', 'test@provider.com');
    await page.fill('[data-testid="password"]', 'test123');
    await page.click('[data-testid="login"]');
    
    await page.waitForSelector('[data-testid="provider-dashboard"]');
    await AccessibilityTestSuite.runAxeTests(page, 'provider dashboard');
  });

  test('WCAG 2.1 AA compliance - Admin panel', async ({ page }) => {
    // Login as admin first
    await page.goto('/admin/login');
    await page.fill('[data-testid="username"]', 'admin@hospital.com');
    await page.fill('[data-testid="password"]', 'admin123');
    await page.click('[data-testid="login"]');
    
    await page.waitForSelector('[data-testid="admin-dashboard"]');
    await AccessibilityTestSuite.runAxeTests(page, 'admin panel');
  });

  test('Keyboard navigation throughout application', async ({ page }) => {
    await AccessibilityTestSuite.testKeyboardNavigation(page);
  });

  test('Screen reader support and ARIA implementation', async ({ page }) => {
    await AccessibilityTestSuite.testScreenReaderSupport(page);
  });

  test('Color contrast and visual design', async ({ page }) => {
    await AccessibilityTestSuite.testColorContrastAndVisualDesign(page);
  });

  test('Mobile accessibility', async ({ page }) => {
    await AccessibilityTestSuite.testMobileAccessibility(page);
  });

  test('Form accessibility features', async ({ page }) => {
    await AccessibilityTestSuite.testFormAccessibility(page);
  });

  test('Skip navigation links', async ({ page }) => {
    await page.goto('/');
    
    // Test skip links (usually hidden until focused)
    await page.keyboard.press('Tab');
    
    const skipLink = await page.locator('a[href="#main-content"], a[href="#main"]').first();
    if (await skipLink.isVisible()) {
      await expect(skipLink).toBeVisible();
      await skipLink.click();
      
      // Verify focus moved to main content
      const mainContent = await page.locator('#main-content, main, #main').first();
      await expect(mainContent).toBeFocused();
    }
  });

  test('Error handling and announcements', async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="start-triage"]');
    
    // Trigger form validation errors
    await page.fill('[data-testid="patient-age"]', 'invalid');
    await page.click('[data-testid="next-step"]');
    
    // Check error announcements
    const errorAnnouncements = await page.locator('[role="alert"], [aria-live="assertive"]').all();
    expect(errorAnnouncements.length).toBeGreaterThan(0);
    
    for (const announcement of errorAnnouncements) {
      await expect(announcement).toBeVisible();
      const text = await announcement.textContent();
      expect(text.trim().length).toBeGreaterThan(0);
    }
  });

  test('High contrast mode support', async ({ page }) => {
    // Simulate high contrast mode
    await page.addStyleTag({
      content: `
        @media (prefers-contrast: high) {
          * {
            border: 2px solid !important;
          }
        }
      `
    });
    
    await page.goto('/');
    await AccessibilityTestSuite.runAxeTests(page, 'high contrast mode');
  });

  test('Reduced motion support', async ({ page }) => {
    // Test prefers-reduced-motion
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/');
    
    // Check that animations are disabled or reduced
    const animatedElements = await page.locator('.animate, .transition, [class*="animate"]').all();
    
    for (const element of animatedElements) {
      const animationDuration = await element.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return computed.animationDuration || computed.transitionDuration;
      });
      
      // Animations should be very short or disabled
      expect(animationDuration === '0s' || animationDuration === 'none').toBe(true);
    }
  });

  test('Text scaling support', async ({ page }) => {
    await page.goto('/');
    
    // Test 200% text scaling
    await page.addStyleTag({
      content: 'html { font-size: 200%; }'
    });
    
    await page.waitForTimeout(1000); // Allow layout to settle
    
    // Check that content is still accessible and doesn't overflow
    const hasHorizontalScroll = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    
    // Horizontal scroll should not be introduced by text scaling
    expect(hasHorizontalScroll).toBe(false);
    
    // Run accessibility tests with scaled text
    await AccessibilityTestSuite.runAxeTests(page, 'scaled text (200%)');
  });

  test('Voice control simulation', async ({ page }) => {
    await page.goto('/');
    
    // Test voice control commands simulation
    const voiceCommands = [
      { command: 'click start triage', target: '[data-testid="start-triage"]' },
      { command: 'click patient name', target: '[data-testid="patient-name"]' },
      { command: 'click next step', target: '[data-testid="next-step"]' }
    ];
    
    for (const voiceCommand of voiceCommands) {
      const element = page.locator(voiceCommand.target);
      
      // Element should be easily identifiable for voice control
      const hasAccessibleName = await element.evaluate(el => {
        return el.getAttribute('aria-label') || 
               el.textContent?.trim() || 
               el.getAttribute('title') ||
               (el.labels && el.labels[0]?.textContent);
      });
      
      expect(hasAccessibleName).toBeTruthy();
    }
  });

  test('International accessibility (i18n)', async ({ page }) => {
    // Test with different languages and RTL support
    await page.addStyleTag({
      content: 'html { direction: rtl; }'
    });
    
    await page.goto('/');
    
    // Check that RTL layout doesn't break accessibility
    await AccessibilityTestSuite.runAxeTests(page, 'RTL layout');
    
    // Verify keyboard navigation still works in RTL
    await page.keyboard.press('Tab');
    const focusedElement = await page.locator(':focus');
    await expect(focusedElement).toBeFocused();
  });

});

// Performance impact test for accessibility features
test.describe('Accessibility Performance Impact', () => {
  
  test('Screen reader performance', async ({ page }) => {
    await page.goto('/');
    
    const startTime = Date.now();
    
    // Simulate screen reader traversal
    const allElements = await page.locator('*').all();
    let accessibleElements = 0;
    
    for (const element of allElements.slice(0, 100)) { // Test first 100 elements
      const isAccessible = await element.evaluate(el => {
        return el.hasAttribute('aria-label') ||
               el.hasAttribute('role') ||
               el.textContent?.trim().length > 0 ||
               el.tagName.match(/^(H[1-6]|P|BUTTON|A|INPUT|SELECT|TEXTAREA)$/);
      });
      
      if (isAccessible) accessibleElements++;
    }
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    // Should process elements quickly
    expect(duration).toBeLessThan(5000); // 5 seconds max
    expect(accessibleElements).toBeGreaterThan(0);
  });

});

module.exports = { AccessibilityTestSuite };