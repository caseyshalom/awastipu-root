/**
 * NotFoundPage — 404 page.
 */


import { Link } from 'react-router-dom';
import { Layout } from '@/components/shared';
import { Button } from '@/components/ui';

export default function NotFoundPage() {
  return (
    <Layout>
      <section className="not-found" id="not-found-page">
        <span className="not-found-icon">🔍</span>
        <h1 className="not-found-title">404</h1>
        <p className="not-found-text">Halaman tidak ditemukan.</p>
        <Link to="/">
          <Button variant="primary">🏠 Kembali ke Beranda</Button>
        </Link>
      </section>
    </Layout>
  );
}
