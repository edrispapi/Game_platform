import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { FiTrendingUp, FiUsers, FiZap, FiShield } from 'react-icons/fi';

const marketingFeatures = [
  {
    icon: <FiTrendingUp className="text-primary text-3xl" />,
    title: 'AI-Powered Creation',
    description:
      'Draft entire gameplay loops, balance mechanics, and produce assets with our AI toolkit.',
  },
  {
    icon: <FiUsers className="text-primary text-3xl" />,
    title: 'Collaborative Workspaces',
    description: 'Invite teammates, co-design in real time, and keep your production pipeline in sync.',
  },
  {
    icon: <FiZap className="text-primary text-3xl" />,
    title: 'Lightning Deployments',
    description: 'Push builds instantly to the Vibe Arcade and gather playtest feedback in minutes.',
  },
  {
    icon: <FiShield className="text-primary text-3xl" />,
    title: 'Secure Distribution',
    description:
      'Ship confidently with role-based access, encrypted assets, and automated QA checks.',
  },
];

const fallbackHomeData = {
  hero: {
    headline: 'Build, test, and launch unforgettable games with an AI-first workflow.',
    subheading:
      'From ideation to live operations, Vibe Coding AI equips studios with collaborative editors, automated asset generation, and actionable analytics.',
    primary_cta: { label: 'Launch Creator Dashboard', href: '/create' },
    secondary_cta: { label: 'Request Studio Access', href: '/signup' },
  },
  trending: [
    {
      title: 'Neon Skyline',
      genre: 'Cyberpunk Strategy',
      description: 'Tactile city building meets noir storytelling in this player-driven metropolis sim.',
    },
    {
      title: 'Echo Drift',
      genre: 'Rhythm Roguelite',
      description: 'Battle distorted echoes with synced combat moves and AI-generated soundscapes.',
    },
    {
      title: 'Starloom',
      genre: 'Co-op Crafting',
      description: 'Warp between biomes, stitch resources, and craft artifacts that reshape the cosmos.',
    },
  ],
  discover: [],
  testimonials: [
    {
      quote:
        '“Vibe Coding AI accelerated our prototype cycles by 3x. The AI co-pilot is a game changer.”',
      author: 'Lena Ortiz — Nebula Forge Studios',
    },
    {
      quote:
        '“From asset generation to analytics, everything our studio needs lives in one polished dashboard.”',
      author: 'James Ahmed — Solarbyte Labs',
    },
    {
      quote:
        '“We launched our community beta in days instead of weeks. The tooling is world-class.”',
      author: 'Mira Chen — Quantum Garden',
    },
  ],
};

const HomePage = () => {
  const [homeData, setHomeData] = useState(fallbackHomeData);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const fetchHomeData = async () => {
      try {
        const response = await fetch('/api/v1/frontend/home');
        if (!response.ok) {
          throw new Error('Unable to load homepage insights.');
        }

        const payload = await response.json();
        if (!isMounted) return;

        setHomeData({
          hero: payload.hero || fallbackHomeData.hero,
          trending: Array.isArray(payload.trending) && payload.trending.length > 0 ? payload.trending : fallbackHomeData.trending,
          discover: Array.isArray(payload.discover) ? payload.discover : [],
          testimonials:
            Array.isArray(payload.testimonials) && payload.testimonials.length > 0
              ? payload.testimonials
              : fallbackHomeData.testimonials,
        });
        setError(null);
      } catch (err) {
        if (!isMounted) return;
        setError(err.message || 'Something went wrong while loading the homepage.');
        setHomeData(fallbackHomeData);
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchHomeData();

    return () => {
      isMounted = false;
    };
  }, []);

  const heroContent = useMemo(() => homeData.hero ?? fallbackHomeData.hero, [homeData.hero]);
  const trendingGames = useMemo(
    () => (homeData.trending?.length ? homeData.trending : fallbackHomeData.trending),
    [homeData.trending]
  );
  const testimonialItems = useMemo(
    () => (homeData.testimonials?.length ? homeData.testimonials : fallbackHomeData.testimonials),
    [homeData.testimonials]
  );

  return (
    <div className="space-y-20 pb-20">
      <section className="pt-20 text-center space-y-8">
        <div className="max-w-4xl mx-auto space-y-6">
          <span className="px-4 py-1 bg-primary/10 text-primary rounded-full text-sm font-semibold">
            Vibe Coding AI Platform
          </span>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight">{heroContent.headline}</h1>
          <p className="text-gray-300 text-lg">{heroContent.subheading}</p>
          <div className="flex justify-center space-x-4">
            <Link
              to={heroContent.primary_cta?.href ?? '/create'}
              className="px-6 py-3 bg-primary hover:bg-secondary transition-colors rounded-lg font-semibold"
            >
              {heroContent.primary_cta?.label ?? 'Launch Creator Dashboard'}
            </Link>
            <Link
              to={heroContent.secondary_cta?.href ?? '/signup'}
              className="px-6 py-3 border border-primary/50 hover:border-secondary transition-colors rounded-lg font-semibold"
            >
              {heroContent.secondary_cta?.label ?? 'Request Studio Access'}
            </Link>
          </div>
          {error && (
            <p className="text-sm text-secondary">{error}</p>
          )}
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-6">
        <h2 className="text-3xl font-bold mb-10">Why studios choose Vibe Coding AI</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {marketingFeatures.map((feature) => (
            <div key={feature.title} className="bg-dark-800 border border-gray-800 rounded-xl p-6 space-y-4">
              <div>{feature.icon}</div>
              <h3 className="text-xl font-semibold">{feature.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-dark-800 border-y border-gray-800 py-16">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold mb-10 text-center">Trending games built with Vibe</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {trendingGames.map((game) => (
              <div key={game.title ?? game.id} className="bg-dark border border-gray-800 rounded-xl p-6 space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-semibold">{game.title}</h3>
                  {game.discount_percent ? (
                    <span className="text-xs font-semibold text-secondary">-{Math.round(game.discount_percent)}%</span>
                  ) : null}
                </div>
                <span className="inline-block text-sm text-primary font-semibold">
                  {game.genre ?? 'Multigenre Experience'}
                </span>
                <p className="text-gray-400 text-sm leading-relaxed">
                  {game.description ?? 'Discover cutting-edge experiences crafted with Vibe Coding AI.'}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {!!homeData.discover?.length && (
        <section className="max-w-6xl mx-auto px-6">
          <div className="flex items-center justify-between mb-10">
            <h2 className="text-3xl font-bold">Fresh releases & recommendations</h2>
            {isLoading && <span className="text-xs text-gray-500">Updating recommendations…</span>}
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {homeData.discover.map((game) => (
              <article key={game.id ?? game.title} className="bg-dark-800 border border-gray-800 rounded-xl p-6 space-y-3">
                <header className="space-y-1">
                  <h3 className="text-xl font-semibold">{game.title}</h3>
                  <p className="text-sm text-gray-400">{game.genre ?? 'Action Adventure'}</p>
                </header>
                <p className="text-sm text-gray-400 leading-relaxed">
                  {game.description ?? 'Personalized recommendation generated from your studio activity.'}
                </p>
                {game.price && (
                  <div className="text-sm text-gray-300">
                    {new Intl.NumberFormat('en-US', {
                      style: 'currency',
                      currency: 'USD',
                    }).format(game.price)}
                  </div>
                )}
              </article>
            ))}
          </div>
        </section>
      )}

      <section className="max-w-5xl mx-auto px-6 text-center space-y-8">
        <h2 className="text-3xl font-bold">Studios scaling with Vibe</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {testimonialItems.map((item, index) => (
            <blockquote
              key={item.author ?? index}
              className="bg-dark-800 border border-gray-800 rounded-xl p-6 space-y-4"
            >
              <p className="text-gray-200 italic">{item.quote}</p>
              <footer className="text-gray-400 text-sm">{item.author ?? 'Vibe Studio'}</footer>
            </blockquote>
          ))}
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 text-center space-y-6">
        <h2 className="text-3xl font-bold">Ready to ship the future of play?</h2>
        <p className="text-gray-300">
          Join a global network of studios building intelligent games with an AI-assisted pipeline.
        </p>
        <Link
          to="/signup"
          className="inline-flex items-center justify-center px-6 py-3 bg-primary hover:bg-secondary transition-colors rounded-lg font-semibold"
        >
          Start your free trial
        </Link>
      </section>
    </div>
  );
};

export default HomePage;
