import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { QueryClient, QueryClientProvider } from "react-query"
import { ReactQueryDevtools } from "react-query/devtools"
import { createBrowserRouter, RouterProvider } from "react-router-dom"

import { Layout } from "Components/Layout"
import { OverviewPage } from "Pages/Overview"
import { SystemPage } from "Pages/System"
import GlobalStyles from "Styles/GlobalStyles"

import { TransactionDetailPage, TransactionListPage } from "./Pages/Transactions"

import "./index.css"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "",
        element: <OverviewPage />,
      },
      {
        path: "transactions/:id",
        element: <TransactionDetailPage />,
      },
      {
        path: "transactions",
        element: <TransactionListPage />,
      },
      {
        path: "system",
        element: <SystemPage />,
      },
    ],
  },
])
const queryClient = new QueryClient()

// Enable mocking in development using msw server set up for the browser
async function enableMocking() {
  if (process.env.DISABLE_MOCKS == "true" || process.env.NODE_ENV !== "development") {
    return
  }

  const { worker, http, HttpResponse } = await import("./tests/mocks/browser")

  // @ts-expect-error This is a wanted violation of Window type, as it is a special env for browser tests.
  // Propagate the worker and `http` references to be globally available.
  // This would allow to modify request handlers on runtime.
  window.msw = {
    worker,
    http,
    HttpResponse,
  }
  return worker.start()
}

void enableMocking().then(() => {
  createRoot(document.getElementById("root")!).render(
    <StrictMode>
      <QueryClientProvider client={queryClient}>
        <GlobalStyles />
        <RouterProvider router={router} />
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </StrictMode>,
  )
})
