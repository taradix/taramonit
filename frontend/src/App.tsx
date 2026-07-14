import { useCallback, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { OverallStatus } from './types'
import StatusPage from './components/StatusPage'
import backgroundImage from "./assets/taram.jpeg";

const API_URL = import.meta.env.VITE_API_URL || 'https://status.taram.ca'

function App() {
  const { t } = useTranslation()
  const [status, setStatus] = useState<OverallStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())

  const fetchStatus = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/api/status`)
      if (!response.ok) {
        throw new Error(t('error.failedToFetch'))
      }
      const data = await response.json()
      setStatus(data)
      setError(null)
      setLastUpdated(new Date())
    } catch (err) {
      setError(err instanceof Error ? err.message : t('error.unknown'))
    } finally {
      setLoading(false)
    }
  }, [t])

  useEffect(() => {
    // fetchStatus is async; its setState calls run after `await fetch`, not
    // synchronously, so the cascading-render concern doesn't apply here.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchStatus()
    // Refresh every 30 seconds
    const interval = setInterval(fetchStatus, 30000)
    return () => clearInterval(interval)
  }, [fetchStatus])

  return (
    <div
      className="min-h-screen bg-zinc-50 text-zinc-900 dark:bg-black dark:text-zinc-100 bg-cover bg-center bg-fixed"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <StatusPage
        status={status}
        loading={loading}
        error={error}
        lastUpdated={lastUpdated}
        onRefresh={fetchStatus}
      />
    </div>
  )
}

export default App
