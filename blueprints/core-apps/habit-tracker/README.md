# 📊 Habit Tracker - Build Better Habits

**Track daily habits, build streaks, and visualize your progress**

Built with KAPI blueprints - Production-ready habit tracking app in 18 minutes.

---

## 🎯 What It Does

A full-featured habit tracking application with:
- **Habit Management**: Create, edit, and organize habits by category
- **Daily Check-ins**: Mark habits complete with one click
- **Streak Tracking**: Current and longest streak calculations
- **Progress Visualization**: Charts and stats showing your consistency
- **Goal Setting**: Weekly targets with progress bars
- **Categories**: Health, Work, Learning, Personal, General

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Node.js 18+
- npm or yarn

### Step 1: Install Dependencies

```bash
npm install
```

### Step 2: Set Up Database

```bash
# Copy environment file
cp .env.example .env

# Initialize SQLite database
npx prisma db push

# (Optional) View database with Prisma Studio
npx prisma studio
```

### Step 3: Run Development Server

```bash
npm run dev
```

Visit **http://localhost:3000** and start tracking your habits!

---

## 📊 Features

### Core Features

#### 1. **Habit Creation**
- Quick templates for common habits (Exercise, Read, Meditate, etc.)
- Custom names, descriptions, and emojis
- Category organization
- Weekly goal setting (1-7 days)
- Color coding for visual organization

#### 2. **Daily Tracking**
- One-click completion toggle
- Visual completion status
- Automatic streak calculation
- Historical completion log

#### 3. **Streak System**
- **Current Streak**: Consecutive days completed
- **Longest Streak**: Best performance record
- **Total Completions**: All-time check-ins
- Maintains streak if completed yesterday (grace period)

#### 4. **Progress Visualization**
- Weekly completion rate charts
- Streak comparison across habits
- Total completions bar charts
- Summary statistics dashboard

#### 5. **Goal Tracking**
- Weekly target setting
- Progress bars for each habit
- Visual completion percentage
- Target vs actual comparison

### UI/UX Features

- **Responsive Design**: Works on mobile, tablet, and desktop
- **Beautiful Gradients**: Category-based color themes
- **Real-time Updates**: Instant UI feedback
- **Quick Stats**: Dashboard overview cards
- **Empty States**: Helpful onboarding for new users

---

## 🏗️ Tech Stack

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Icon library
- **Recharts**: Data visualization

### Backend
- **Next.js API Routes**: Serverless functions
- **Prisma ORM**: Type-safe database access
- **SQLite**: Default database (easy setup)
- **PostgreSQL**: Production option

### Data Management
- **Zod**: Runtime validation
- **React Hook Form**: Form handling
- **date-fns**: Date manipulation

---

## 📁 Project Structure

```
habit-tracker/
├── app/
│   ├── api/
│   │   └── habits/
│   │       ├── route.ts          # List/create habits
│   │       └── [id]/
│   │           └── complete/
│   │               └── route.ts  # Toggle completion
│   ├── page.tsx                  # Main dashboard
│   ├── layout.tsx                # Root layout
│   └── globals.css               # Global styles
├── components/
│   ├── HabitCard.tsx             # Individual habit display
│   ├── HabitForm.tsx             # Create habit form
│   └── ProgressChart.tsx         # Charts and stats
├── lib/
│   └── streak-calculator.ts      # Streak logic utilities
├── schema.prisma                 # Database schema
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

---

## 🗄️ Database Schema

### Habit Model
```prisma
model Habit {
  id          String   @id @default(cuid())
  name        String
  description String?
  category    String   @default("general")
  color       String   @default("#3B82F6")
  icon        String?
  targetDays  Int      @default(7)
  frequency   String   @default("daily")
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  archived    Boolean  @default(false)

  completions Completion[]
  reminders   Reminder[]
}
```

### Completion Model
```prisma
model Completion {
  id        String   @id @default(cuid())
  habitId   String
  date      DateTime
  note      String?
  createdAt DateTime @default(now())

  habit     Habit    @relation(...)

  @@unique([habitId, date])
}
```

---

## 🔧 API Reference

### GET /api/habits
List all habits with calculated stats.

**Response:**
```json
[
  {
    "id": "clxxx",
    "name": "Morning Run",
    "category": "health",
    "color": "#10B981",
    "icon": "🏃",
    "currentStreak": 7,
    "longestStreak": 14,
    "isCompletedToday": true,
    "totalCompletions": 42
  }
]
```

### POST /api/habits
Create a new habit.

**Request:**
```json
{
  "name": "Read for 30 min",
  "description": "Daily reading habit",
  "category": "learning",
  "color": "#8B5CF6",
  "icon": "📚",
  "targetDays": 7
}
```

### POST /api/habits/[id]/complete
Mark habit as complete for a specific date.

**Request:**
```json
{
  "date": "2025-10-02T00:00:00.000Z",
  "note": "Finished 'Atomic Habits' chapter 3"
}
```

### DELETE /api/habits/[id]/complete?date=2025-10-02
Remove completion for a specific date.

---

## 🧮 Streak Calculation Algorithm

The streak calculator uses sophisticated logic to determine streaks:

### Current Streak
1. Start from today
2. If not completed today, check yesterday (grace period)
3. Count consecutive days backward
4. Stop at first gap

### Longest Streak
1. Scan all completion dates
2. Find longest consecutive sequence
3. Compare with current streak
4. Return maximum

### Example:
```
Completions: Oct 2, Oct 1, Sep 30, Sep 28, Sep 27

Current streak: 3 days (Oct 2, 1, 30)
Longest streak: 3 days (same sequence)
```

---

## 🎨 Customization

### Change Categories

Edit `components/HabitForm.tsx`:

```typescript
const CATEGORIES = [
  { value: 'fitness', label: '💪 Fitness', color: '#10B981' },
  { value: 'mindfulness', label: '🧘 Mindfulness', color: '#8B5CF6' },
  // Add your own...
];
```

### Add Quick Templates

```typescript
const COMMON_HABITS = [
  { name: 'Morning Pages', icon: '✍️', category: 'personal' },
  { name: 'Cold Shower', icon: '🚿', category: 'health' },
  // Add your favorites...
];
```

### Switch to PostgreSQL

1. Update `.env`:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/habit_tracker"
```

2. Update `schema.prisma`:
```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

3. Push schema:
```bash
npx prisma db push
```

---

## 📈 Progress Tracking

### Weekly Completion Rate
Line chart showing:
- Actual completions per week
- Target completion line
- Trend over 4-12 weeks

### Streak Comparison
Bar chart comparing:
- Current streaks across all habits
- Identify strongest/weakest habits

### Total Completions
Bar chart showing:
- All-time completions per habit
- Overall consistency

### Summary Statistics
- Average streak length
- Total check-ins
- Active habits (with current streaks)
- Consistency percentage (7+ day streaks)

---

## 🚀 Deployment

### Option 1: Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set up PostgreSQL database (Vercel Postgres)
# Add DATABASE_URL to environment variables
```

### Option 2: Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npx prisma generate
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

```bash
docker build -t habit-tracker .
docker run -p 3000:3000 habit-tracker
```

### Option 3: Traditional Hosting

```bash
# Build for production
npm run build

# Start production server
npm start
```

---

## 🔮 Future Enhancements

### MVP+ Features (Next 18 min)
- [ ] **Reminders**: Browser notifications at set times
- [ ] **Notes**: Add context to daily completions
- [ ] **Calendar Heat Map**: GitHub-style contribution graph
- [ ] **Export Data**: CSV download of completion history
- [ ] **Habit Editing**: Update existing habits
- [ ] **Archive Habits**: Soft delete completed goals

### Advanced Features (Future Sprints)
- [ ] **Multi-user Support**: User authentication
- [ ] **Habit Sharing**: Share goals with friends
- [ ] **Social Features**: Leaderboards, challenges
- [ ] **Advanced Analytics**: Correlation between habits
- [ ] **Mobile App**: React Native version
- [ ] **Integrations**: Apple Health, Google Fit
- [ ] **AI Insights**: Personalized recommendations

---

## 🐛 Troubleshooting

### Database Issues

**Error: Can't reach database**
```bash
# Reset database
rm prisma/dev.db
npx prisma db push
```

**Error: Prisma Client not found**
```bash
# Regenerate Prisma Client
npx prisma generate
```

### Build Errors

**TypeScript errors**
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

**Missing dependencies**
```bash
# Reinstall all packages
rm -rf node_modules package-lock.json
npm install
```

---

## 📚 Learning Resources

**Habit Formation Science**:
- "Atomic Habits" by James Clear
- "The Power of Habit" by Charles Duhigg
- [Habit Formation Research](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3505409/)

**Tech Stack Documentation**:
- [Next.js 14 Docs](https://nextjs.org/docs)
- [Prisma Guide](https://www.prisma.io/docs)
- [Recharts Examples](https://recharts.org/en-US/examples)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## 🎓 Educational Value

This project demonstrates:

### 1. **Full-Stack Development**
- Next.js App Router patterns
- Server-side API routes
- Client-side state management
- Database design and queries

### 2. **Data Modeling**
- Time-series data (completions over time)
- Relationship modeling (habits → completions)
- Unique constraints for data integrity
- Efficient indexing strategies

### 3. **Algorithms**
- Streak calculation logic
- Date manipulation and normalization
- Statistical aggregations
- Performance optimization

### 4. **UI/UX Patterns**
- Gamification (streaks, progress bars)
- Data visualization (charts, heat maps)
- Form handling and validation
- Responsive design

---

## 📄 License

MIT - Free for personal and commercial use

---

## 🙏 Acknowledgments

- **Inspiration**: Habitica, Streaks, Loop Habit Tracker
- **Design**: Tailwind UI patterns
- **Icons**: Lucide React
- **Charts**: Recharts library
- **Built with**: KAPI Production Blueprints

---

**Built with KAPI** - From idea to production in 18 minutes

**Questions?** Check the code comments for detailed explanations.
