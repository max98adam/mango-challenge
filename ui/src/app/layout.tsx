import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

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
        <header className="text-5xl p-4 flex justify-start">
          <Link href={"/"}>MM Fashion 🥭</Link>
        </header>
        {children}
      </body>
    </html>
  );
}
