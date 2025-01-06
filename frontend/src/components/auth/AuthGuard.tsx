'use client';

import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import MainLayout from '@/components/layout/MainLayout';
import { Spin } from 'antd';

const PUBLIC_PATHS = ['/login'];

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) {
    return <Spin className="flex justify-center items-center min-h-screen" />;
  }

  // 登录页面使用独立布局
  if (PUBLIC_PATHS.includes(pathname)) {
    return <>{children}</>;
  }

  // 其他页面使用主布局
  return <MainLayout>{children}</MainLayout>;
} 