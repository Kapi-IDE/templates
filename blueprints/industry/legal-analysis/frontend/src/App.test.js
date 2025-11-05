import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

describe('Legal Analysis UI', () => {
  beforeEach(() => {
    global.fetch = jest.fn((url, options) => {
      if (url.endsWith('/api/health')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ status: 'healthy' }),
        });
      }
      if (url.endsWith('/api/research')) {
        return Promise.resolve({
          ok: true,
          json: () =>
            Promise.resolve({
              analysis: 'Stub research memo',
              structured: { legal_issues: ['issue'] },
              authorities: [],
            }),
        });
      }
      if (url.endsWith('/api/precedents/search')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ precedents: [] }),
        });
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ cases: [] }),
      });
    });
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('renders navigation tabs and switches panels', async () => {
    render(<App />);

    await waitFor(() => expect(screen.getByText(/Legal Analysis Blueprint/i)).toBeInTheDocument());
    expect(screen.getByRole('button', { name: /Research/i })).toHaveClass('active');

    fireEvent.click(screen.getByRole('button', { name: /Cases/i }));
    expect(screen.getByRole('button', { name: /Cases/i })).toHaveClass('active');
  });
});
