'use client'

/**
 * Error Boundary Component
 * 捕獲 React 元件樹中的錯誤並顯示優雅的錯誤訊息
 */

import React, { ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // 記錄錯誤到控制台供調試
    console.error('Error caught by ErrorBoundary:', error, errorInfo)
  }

  handleRetry = () => {
    // 重新載入頁面
    window.location.reload()
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
            <div className="flex justify-center mb-4">
              <div className="text-6xl">⚠️</div>
            </div>
            <h1 className="text-2xl font-bold text-red-600 mb-4 text-center">
              出錯了
            </h1>
            <p className="text-gray-700 mb-6 text-center">
              儀表板在載入過程中發生問題。請重新嘗試或聯絡支援。
            </p>
            {process.env.NODE_ENV === 'development' && (
              <div className="bg-red-50 border border-red-200 rounded p-4 mb-6">
                <p className="text-sm font-mono text-red-700 break-words">
                  {this.state.error?.message}
                </p>
              </div>
            )}
            <button
              onClick={this.handleRetry}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors"
            >
              重新載入頁面
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
