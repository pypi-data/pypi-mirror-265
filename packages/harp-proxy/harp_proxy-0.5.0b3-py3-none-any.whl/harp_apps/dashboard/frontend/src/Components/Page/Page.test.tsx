import { render, screen } from "@testing-library/react"
import { ErrorBoundary } from "react-error-boundary"
import { afterEach, describe, expect, test, vi } from "vitest"

import { Error as ErrorFunc, Page } from "./Page.tsx"
import { PageTitle } from "./PageTitle.tsx"

describe("Page", () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  test("renders without error", () => {
    const { container } = render(
      <Page children={<div />} title={<PageTitle title="Test Title" description="Test Description" />} />,
    )
    expect(container).toMatchSnapshot()
  })

  test("renders title and description", () => {
    render(<Page children={<div />} title={<PageTitle title="Test Title" description="Test Description" />} />)
    expect(screen.getByText("Test Title")).toBeInTheDocument()
    expect(screen.getByText("Test Description")).toBeInTheDocument()
  })

  test("renders Error component when child throws error", () => {
    vi.spyOn(console, "error").mockImplementation(() => {})
    const Child = () => {
      throw new Error("Test error")
    }

    render(
      <ErrorBoundary FallbackComponent={ErrorFunc}>
        <Page children={<Child />} />
      </ErrorBoundary>,
    )

    expect(screen.getByText("Woopsie!")).toBeInTheDocument()
    expect(screen.getByText("An error has occurred in this component.")).toBeInTheDocument()
  })
})
