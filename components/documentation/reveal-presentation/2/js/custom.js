// Handle user flow diagram animations
function initUserFlowDiagram() {
  // This function will be called when the slide with the user flow is shown
  console.log('Initializing user flow diagram animations');
  
  // Variables to track the current stage
  let currentStage = 'engineer';
  const stages = ['engineer', 'search', 'analysis', 'apply'];
  let currentIndex = 0;
  
  // Initialize navigation
  const container = document.querySelector('.user-flow-container');
  const prevButton = container.querySelector('.flow-nav.prev');
  const nextButton = container.querySelector('.flow-nav.next');
  
  // Function to update the visible stage
  function updateStage(newIndex) {
    // Bounds check
    if (newIndex < 0 || newIndex >= stages.length) {
      return;
    }
    
    // Update index and stage
    currentIndex = newIndex;
    currentStage = stages[currentIndex];
    
    // Hide all stages and progress indicators
    document.querySelectorAll('.flow-stage').forEach(el => {
      el.classList.remove('visible');
    });
    document.querySelectorAll('.progress-dot').forEach(el => {
      el.classList.remove('active');
    });
    
    // Show current stage and update progress indicator
    const stageEl = document.querySelector(`.flow-stage.${currentStage}`);
    const dotEl = document.querySelector(`.progress-dot.${currentStage}`);
    
    if (stageEl) stageEl.classList.add('visible');
    if (dotEl) dotEl.classList.add('active');
    
    // Update nav buttons visibility
    prevButton.classList.toggle('visible', currentIndex > 0);
    nextButton.classList.toggle('visible', currentIndex < stages.length - 1);
  }
  
  // Set up navigation handlers
  prevButton.addEventListener('click', function() {
    updateStage(currentIndex - 1);
  });
  
  nextButton.addEventListener('click', function() {
    updateStage(currentIndex + 1);
  });
  
  // Handle keyboard navigation
  document.addEventListener('keydown', function(e) {
    // Only handle when on user workflow slide
    if (!container.parentElement.classList.contains('present')) {
      return;
    }
    
    // Arrow keys for navigation
    if (e.key === 'ArrowLeft') {
      updateStage(currentIndex - 1);
      e.preventDefault();
    } else if (e.key === 'ArrowRight') {
      updateStage(currentIndex + 1);
      e.preventDefault();
    }
  });
  
  // Add click handlers to progress dots
  document.querySelectorAll('.progress-dot').forEach(function(dot, index) {
    dot.addEventListener('click', function() {
      updateStage(index);
    });
  });
  
  // Initialize with the first stage
  updateStage(0);
}

// Handle architecture diagram animations
function initArchitectureDiagram() {
  // This function will be called when the slide with the architecture is shown
  console.log('Initializing architecture diagram animations');
  
  // Add interactive hover effects to architecture components
  document.querySelectorAll('.arch-component').forEach(function(component) {
    component.addEventListener('mouseenter', function() {
      component.style.transform = 'translateY(-5px) scale(1.05)';
      component.style.backgroundColor = 'rgba(255, 255, 255, 0.18)';
      component.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.3)';
    });
    
    component.addEventListener('mouseleave', function() {
      component.style.transform = '';
      component.style.backgroundColor = '';
      component.style.boxShadow = '';
    });
  });
  
  // Add interactive hover effects to security components
  document.querySelectorAll('.sec-comp-component').forEach(function(component) {
    component.addEventListener('mouseenter', function() {
      component.style.transform = 'translateY(-5px)';
      component.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
      component.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.3)';
      component.style.color = 'rgba(3, 218, 198, 1)';
      
      // Highlight all bidirectional arrows
      document.querySelectorAll('.bidir-arrow-down').forEach(function(arrow) {
        arrow.style.backgroundColor = 'rgba(3, 218, 198, 1)';
        arrow.style.boxShadow = '0 0 10px rgba(3, 218, 198, 0.6)';
        arrow.style.width = '3px';
      });
    });
    
    component.addEventListener('mouseleave', function() {
      component.style.transform = '';
      component.style.backgroundColor = '';
      component.style.boxShadow = '';
      component.style.color = '';
      
      // Reset all bidirectional arrows
      document.querySelectorAll('.bidir-arrow-down').forEach(function(arrow) {
        arrow.style.backgroundColor = '';
        arrow.style.boxShadow = '';
        arrow.style.width = '';
      });
    });
  });
  
  // Show the security section after the main architecture components
  Reveal.addEventListener('fragmentshown', function(event) {
    const fragment = event.fragment;
    
    if (fragment.classList.contains('security-compliance')) {
      // Ensure the section and all arrows get their visible classes
      fragment.classList.add('visible');
      
      // Make all arrows visible
      document.querySelectorAll('.bidir-arrow-down').forEach(function(arrow) {
        if (arrow.classList.contains('fragment') && arrow.classList.contains('fade-in')) {
          arrow.classList.add('visible');
        }
      });
      
      // Add a slight animation to each security component
      document.querySelectorAll('.sec-comp-component').forEach(function(component, index) {
        setTimeout(function() {
          component.style.animation = 'fadeInUp 0.4s ease-out forwards';
        }, 100 + (index * 80));
      });
    }
  });
}

// Handle business benefits interactions
function initBusinessBenefits() {
  // This function will be called when the slide with business benefits is shown
  console.log('Initializing business benefits animations');
  
  // Add pulse effect to metrics when they appear
  document.querySelectorAll('.benefit-metric').forEach(function(metric) {
    // Add a pulse animation class when the parent fragment is visible
    const parentFragment = metric.closest('.fragment');
    if (parentFragment) {
      const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
          if (mutation.attributeName === 'class') {
            if (parentFragment.classList.contains('visible')) {
              metric.classList.add('pulse-animation');
              setTimeout(() => metric.classList.remove('pulse-animation'), 1500);
            }
          }
        });
      });
      
      observer.observe(parentFragment, { attributes: true });
    }
  });
  
  // Add hover effects for benefit items
  document.querySelectorAll('.benefit-item').forEach(function(item) {
    item.addEventListener('mouseenter', function() {
      item.style.transform = 'translateY(-8px)';
      item.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.4)';
      
      // Highlight the metric value
      const metric = item.querySelector('.benefit-metric');
      if (metric) {
        metric.style.fontSize = '2.4em';
        metric.style.color = '#e9c4ff';
      }
    });
    
    item.addEventListener('mouseleave', function() {
      item.style.transform = '';
      item.style.boxShadow = '';
      
      // Reset the metric value
      const metric = item.querySelector('.benefit-metric');
      if (metric) {
        metric.style.fontSize = '';
        metric.style.color = '';
      }
    });
  });
}

// Wait for the presentation to be fully loaded
window.addEventListener('load', function() {
  // Handle slide-specific styling
  function handleSlideStyles() {
    const currentIndex = Reveal.getIndices().h;
    const revealElement = document.querySelector('.reveal');
    
    // Set data attribute for current slide number for CSS targeting
    revealElement.setAttribute('data-slide-number', currentIndex);
    
    // Add special class to body for first slide
    if (currentIndex === 0) {
      document.body.classList.add('on-title-slide');
    } else {
      document.body.classList.remove('on-title-slide');
    }
  }

  // Call on slide change
  Reveal.addEventListener('slidechanged', handleSlideStyles);
  
  // Initial call after load
  setTimeout(handleSlideStyles, 500);

  // Add event listener for keyboard shortcuts
  document.addEventListener('keydown', function(event) {
    // Alt+D to toggle dark mode
    if (event.altKey && event.key === 'd') {
      toggleDarkMode();
    }
    // Alt+F to toggle fullscreen
    if (event.altKey && event.key === 'f') {
      toggleFullScreen();
    }
  });

  // Add dark mode toggle button
  const darkModeButton = document.createElement('div');
  darkModeButton.innerHTML = '☀️'; // Sun icon for dark mode
  darkModeButton.className = 'dark-mode-toggle';
  darkModeButton.title = 'Toggle Dark/Light Mode (Alt+D)';
  darkModeButton.addEventListener('click', toggleDarkMode);
  document.body.appendChild(darkModeButton);

  // Add fullscreen button
  const fullScreenButton = document.createElement('div');
  fullScreenButton.innerHTML = '⛶'; 
  fullScreenButton.className = 'fullscreen-toggle';
  fullScreenButton.title = 'Toggle Fullscreen (Alt+F)';
  fullScreenButton.addEventListener('click', toggleFullScreen);
  document.body.appendChild(fullScreenButton);

  // Add speaker view button
  const speakerViewButton = document.createElement('div');
  speakerViewButton.innerHTML = '👁️';
  speakerViewButton.className = 'speaker-view-toggle';
  speakerViewButton.title = 'Open Speaker View';
  speakerViewButton.addEventListener('click', function() {
    window.open('?view=speaker', 'speaker-view', 'width=1000,height=700');
  });
  document.body.appendChild(speakerViewButton);
});

// Toggle between dark and light mode
function toggleDarkMode() {
  const theme = document.getElementById('theme');
  const currentTheme = theme.getAttribute('href');
  
  if (currentTheme.includes('black')) {
    theme.setAttribute('href', 'https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/white.css');
    document.querySelector('.dark-mode-toggle').innerHTML = '🌙';
  } else {
    theme.setAttribute('href', 'https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/black.css');
    document.querySelector('.dark-mode-toggle').innerHTML = '☀️';
  }
}

// Toggle fullscreen
function toggleFullScreen() {
  if (!document.fullscreenElement &&    // Standard property
      !document.mozFullScreenElement && // Firefox
      !document.webkitFullscreenElement && // Chrome, Safari and Opera
      !document.msFullscreenElement) {  // IE/Edge
    
    // Enter fullscreen
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen();
    } else if (document.documentElement.mozRequestFullScreen) { // Firefox
      document.documentElement.mozRequestFullScreen();
    } else if (document.documentElement.webkitRequestFullscreen) { // Chrome, Safari and Opera
      document.documentElement.webkitRequestFullscreen();
    } else if (document.documentElement.msRequestFullscreen) { // IE/Edge
      document.documentElement.msRequestFullscreen();
    }
    document.querySelector('.fullscreen-toggle').innerHTML = '⛋';
  } else {
    // Exit fullscreen
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) { // Firefox
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) { // Chrome, Safari and Opera
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { // IE/Edge
      document.msExitFullscreen();
    }
    document.querySelector('.fullscreen-toggle').innerHTML = '⛶';
  }
}

// Listen for slide change events
document.addEventListener('DOMContentLoaded', function() {
  if (typeof Reveal !== 'undefined') {
    Reveal.addEventListener('slidechanged', function(event) {
      // Check if this is the user flow slide
      const currentSlide = event.currentSlide;
      if (currentSlide.querySelector('.workflow-diagram')) {
        initUserFlowDiagram();
      }
      
      // Check if this is the architecture slide
      if (currentSlide.querySelector('.architecture-container')) {
        initArchitectureDiagram();
      }
      
      // Check if this is the business benefits slide
      if (currentSlide.querySelector('.business-benefits-container')) {
        initBusinessBenefits();
      }
      
      // Check if this is the combined benefits slide
      if (currentSlide.querySelector('.combined-benefits-container')) {
        initCombinedBenefits();
      }
      
      // Check if this is the cluster analysis slide
      if (currentSlide.querySelector('.cluster-analysis-container')) {
        initClusterAnalysis();
      }
    });

    // Handle fragment animations
    Reveal.addEventListener('fragmentshown', function(event) {
      const fragment = event.fragment;
      
      // For user flow details animation
      if (fragment.classList.contains('flow-detail')) {
        // Add visible class to show the detail
        fragment.classList.add('visible');
      }
      
      // For chart animations
      if (fragment.classList.contains('chart-animation')) {
        animateCharts(fragment);
      }
    });

    Reveal.addEventListener('fragmenthidden', function(event) {
      const fragment = event.fragment;
      
      // For user flow details animation
      if (fragment.classList.contains('flow-detail')) {
        // Remove visible class to hide the detail
        fragment.classList.remove('visible');
      }
    });
  }
});

// Simple function to animate charts
function animateCharts(element) {
  // This would be replaced with actual chart animation code
  console.log('Animating chart', element);
}

// Handle combined benefits interactions
function initCombinedBenefits() {
  // This function will be called when the slide with the combined benefits is shown
  console.log('Initializing combined benefits animations');
  
  // Add animated entrance and interactions to the combined benefit items
  const benefitItems = document.querySelectorAll('.combined-benefit-item');
  
  // Set up animated entrance with staggered delays
  benefitItems.forEach(function(item, index) {
    // Add observer to detect when fragments become visible
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.attributeName === 'class') {
          if (item.classList.contains('visible')) {
            // Add entrance animation with staggered delay
            item.style.animation = `slide-in-bottom 0.6s ease-out ${index * 0.15}s forwards`;
            
            // Add pulse animation to the metric after a delay
            const metric = item.querySelector('.benefit-metric');
            if (metric) {
              setTimeout(function() {
                metric.classList.add('pulse-animation');
              }, 500 + (index * 150));
            }
          }
        }
      });
    });
    
    observer.observe(item, { attributes: true });
  });
  
  // Add hover effects
  benefitItems.forEach(function(item) {
    item.addEventListener('mouseenter', function() {
      // Enhance the highlighted item
      item.style.background = 'rgba(187, 134, 252, 0.1)';
      item.style.transform = 'translateY(-10px)';
      item.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.4)';
      
      // Make the border glow
      item.style.borderColor = 'rgba(187, 134, 252, 0.6)';
      
      // Activate the top gradient line
      item.style.setProperty('--gradient-opacity', '1');
      
      // Make other items slightly fade out
      benefitItems.forEach(function(otherItem) {
        if (otherItem !== item) {
          otherItem.style.opacity = '0.6';
          otherItem.style.filter = 'blur(1px)';
          otherItem.style.transform = 'scale(0.98)';
        }
      });
    });
    
    item.addEventListener('mouseleave', function() {
      // Reset this item
      item.style.background = '';
      item.style.transform = '';
      item.style.boxShadow = '';
      item.style.borderColor = '';
      item.style.setProperty('--gradient-opacity', '');
      
      // Reset other items
      benefitItems.forEach(function(otherItem) {
        otherItem.style.opacity = '';
        otherItem.style.filter = '';
        otherItem.style.transform = '';
      });
    });
  });
}

// Handle cluster analysis interactions
function initClusterAnalysis() {
  // This function will be called when the slide with the cluster analysis is shown
  console.log('Initializing cluster analysis animations');
  
  // Add interactive hover effects to cluster components
  document.querySelectorAll('.cluster-component').forEach(function(component) {
    component.addEventListener('mouseenter', function() {
      component.style.transform = 'translateY(-5px) scale(1.05)';
      component.style.backgroundColor = 'rgba(255, 255, 255, 0.18)';
      component.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.3)';
    });
    
    component.addEventListener('mouseleave', function() {
      component.style.transform = '';
      component.style.backgroundColor = '';
      component.style.boxShadow = '';
    });
  });
  
  // Add interactive hover effects to methodology components
  document.querySelectorAll('.method-component').forEach(function(component) {
    component.addEventListener('mouseenter', function() {
      component.style.transform = 'translateY(-5px)';
      component.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
      component.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.3)';
      component.style.color = 'rgba(187, 134, 252, 1)';
    });
    
    component.addEventListener('mouseleave', function() {
      component.style.transform = '';
      component.style.backgroundColor = '';
      component.style.boxShadow = '';
      component.style.color = '';
    });
  });
  
  // Handle fragment animations
  Reveal.addEventListener('fragmentshown', function(event) {
    const fragment = event.fragment;
    
    if (fragment.classList.contains('cluster-section') || fragment.classList.contains('cluster-section-wide')) {
      // Add visible class for the section
      fragment.classList.add('visible');
      
      // Find any related arrows and make them visible
      if (fragment.classList.contains('differentiator')) {
        const arrow = document.querySelector('.cluster-arrow[style*="left: 280px"]');
        if (arrow) arrow.classList.add('visible');
      } else if (fragment.classList.contains('results')) {
        const arrow = document.querySelector('.cluster-arrow[style*="left: 580px"]');
        if (arrow) arrow.classList.add('visible');
      } else if (fragment.classList.contains('value')) {
        const arrow = document.querySelector('.cluster-arrow[style*="left: 880px"]');
        if (arrow) arrow.classList.add('visible');
      }
      
      // Add a slight animation to each component
      fragment.querySelectorAll('.cluster-component, .method-component').forEach(function(component, index) {
        setTimeout(function() {
          component.style.animation = 'fadeInUp 0.4s ease-out forwards';
        }, 100 + (index * 80));
      });
    }
  });
}