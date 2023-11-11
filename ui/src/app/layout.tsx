import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Mango MM Fashion",
  description: "Outfit recommendation app",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen  w-full flex flex-col`}>
        <header className="text-5xl p-4">MM Fashion 🥭</header>
        {children}
      </body>
    </html>
  );
}
