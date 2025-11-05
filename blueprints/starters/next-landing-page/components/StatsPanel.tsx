const stats = [
  { value: '12 hrs', label: 'Average launch time' },
  { value: '9 sections', label: 'Reusable building blocks' },
  { value: 'MIT', label: 'Permissive license' },
];

export function StatsPanel() {
  return (
    <section className="border-y border-white/10">
      <div className="mx-auto grid max-w-4xl grid-cols-1 divide-y divide-white/10 px-6 py-14 sm:grid-cols-3 sm:divide-x sm:divide-y-0 sm:px-10">
        {stats.map((stat) => (
          <div key={stat.label} className="flex flex-col items-center gap-2 py-6 text-center">
            <span className="text-3xl font-semibold text-white">{stat.value}</span>
            <span className="text-xs uppercase tracking-[0.2em] text-white/50">{stat.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
