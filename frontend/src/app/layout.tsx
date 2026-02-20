import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Jira Dashboard MVP',
  description: 'Jira Dashboard for project metrics and status tracking',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW">
      <body>{children}</body>
    </html>
  )
}
