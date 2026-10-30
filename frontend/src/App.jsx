import { useMemo, useState } from 'react'

const pages = [
  'Connect Accounts',
  'Overview',
  'Issues',
  'Action Queue',
  'Content',
  'Reviews',
  'Ads',
  'Reports',
  'Settings',
]

function App() {
  const [active, setActive] = useState('Overview')
  const [automationMode, setAutomationMode] = useState({
    searchConsole: 'manual',
    sitemap: 'manual',
    ads: 'manual',
    gbp: 'manual',
  })

  const summaryCards = useMemo(
    () => [
      { title: 'Organic Clicks', value: '12.4k', change: '+8.2%' },
      { title: 'Avg Rank', value: '9.1', change: '+1.4' },
      { title: 'Ad Spend', value: '$2,920', change: '-11.3%' },
      { title: 'Open Issues', value: '7', change: '-2' },
    ],
    [],
  )

  return (
    <div className="min-h-screen">
      <header className="border-b bg-white px-6 py-4">
        <h1 className="m-0 text-2xl font-semibold">SEO & Ads Optimization Agent</h1>
        <p className="mt-1 text-sm text-slate-600">Mock dashboard in demo mode</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-[260px,1fr]">
        <aside className="border-r bg-white p-3">
          <nav className="grid gap-1">
            {pages.map((page) => (
              <button
                key={page}
                onClick={() => setActive(page)}
                className={`rounded-md px-3 py-2 text-left text-sm ${
                  active === page ? 'bg-indigo-600 text-white' : 'bg-slate-50 text-slate-700 hover:bg-slate-100'
                }`}
              >
                {page}
              </button>
            ))}
          </nav>
        </aside>

        <main className="p-6">
          {active === 'Overview' && (
            <section>
              <div className="mb-4 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                {summaryCards.map((card) => (
                  <article key={card.title} className="rounded-lg border bg-white p-4 shadow-sm">
                    <h2 className="m-0 text-sm text-slate-500">{card.title}</h2>
                    <p className="my-2 text-2xl font-semibold">{card.value}</p>
                    <p className="m-0 text-sm text-emerald-600">{card.change}</p>
                  </article>
                ))}
              </div>
              <div className="rounded-lg border bg-white p-4">
                <h3 className="m-0 text-lg font-medium">Weekly Priority Plan</h3>
                <ul className="mt-3 list-disc pl-6 text-sm text-slate-700">
                  <li>Improve low CTR pages with refreshed title/meta suggestions</li>
                  <li>Fix broken links and missing schema from technical crawl</li>
                  <li>Review ad search terms for wasted spend and negatives</li>
                </ul>
              </div>
            </section>
          )}

          {active === 'Action Queue' && (
            <section className="rounded-lg border bg-white p-4">
              <h3 className="m-0 text-lg font-medium">Approval Queue</h3>
              <p className="mt-2 text-sm text-slate-600">
                Manual mode by default. Spend-increasing actions stay blocked unless full-auto is enabled.
              </p>
            </section>
          )}

          {active === 'Settings' && (
            <section className="rounded-lg border bg-white p-4">
              <h3 className="m-0 text-lg font-medium">Automation Levels</h3>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                {Object.keys(automationMode).map((moduleKey) => (
                  <label key={moduleKey} className="grid gap-1 text-sm">
                    <span className="capitalize">{moduleKey}</span>
                    <select
                      className="rounded-md border p-2"
                      value={automationMode[moduleKey]}
                      onChange={(e) =>
                        setAutomationMode((current) => ({ ...current, [moduleKey]: e.target.value }))
                      }
                    >
                      <option value="manual">Manual</option>
                      <option value="semi_auto">Semi-auto</option>
                      <option value="full_auto">Full-auto</option>
                    </select>
                  </label>
                ))}
              </div>
            </section>
          )}

          {!['Overview', 'Action Queue', 'Settings'].includes(active) && (
            <section className="rounded-lg border bg-white p-4 text-sm text-slate-700">
              {active} page scaffold is ready for module-specific integrations.
            </section>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
