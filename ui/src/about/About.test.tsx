import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";
import { fakeService, renderApp } from "../testing";

for (const language of ["en", "ar"] as const) {
  test(`About shows the MIT notice and candidate font notices in ${language}`, async () => {
    fakeService({
      "GET /settings": () => ({ language, theme: "light", ai: null }),
      "GET /about": () => ({ version: "0.1.0", data_folder: "/synthetic/.tawreed" }),
    });
    renderApp();
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: language === "en" ? "About" : "حول توريد" }));
    expect(await screen.findByText(language === "en" ? "MIT License © 2026 QS Mind." : "رخصة MIT © 2026 كيو إس مايند.")).toBeInTheDocument();
    expect(screen.queryByText(/All rights reserved|جميع الحقوق محفوظة/)).not.toBeInTheDocument();
    expect(screen.getByText(/Figtree/)).toBeInTheDocument();
    expect(screen.getByText(language === "en" ? /Arabic uses the system font/ : /العربية تستخدم خط النظام/)).toBeInTheDocument();
  });
}
