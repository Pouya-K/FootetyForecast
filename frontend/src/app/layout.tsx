import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FooteyForecast",
  description: "Premier League match predictions powered by ML",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
