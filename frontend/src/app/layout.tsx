import { Inter } from 'next/font/google';
import { AntdRegistry } from '@ant-design/nextjs-registry';
import AuthGuard from '../components/auth/AuthGuard';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: '教育辅助系统',
  description: '多模态教育教学辅助系统',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh">
      <body className={inter.className}>
        <AntdRegistry>
          <AuthGuard>{children}</AuthGuard>
        </AntdRegistry>
      </body>
    </html>
  );
} 