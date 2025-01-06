import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const PUBLIC_PATHS = ['/login', '/', '/favicon.ico'];

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token');
  const { pathname } = request.nextUrl;

  // 如果是根路径，重定向到登录页
  if (pathname === '/') {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 如果是公开路径，直接通过
  if (PUBLIC_PATHS.includes(pathname)) {
    return NextResponse.next();
  }

  // 如果没有token且不是公开路径，重定向到登录页
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 如果有token且访问登录页，重定向到仪表盘
  if (token && pathname === '/login') {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * 匹配所有路径除了:
     * /api/* (API 路由)
     * /_next/static (静态文件)
     * /_next/image (图片优化)
     * /favicon.ico (浏览器图标)
     */
    '/((?!api|_next/static|_next/image|.*\\..*|api|_next).*)'
  ]
}; 