import { Link } from 'react-router-dom';
import { FiTrendingUp, FiUsers, FiZap, FiShield } from 'react-icons/fi';

const features = [
  {
    icon: <FiTrendingUp className="text-primary text-3xl" />,
    title: 'AI-Powered Creation',
    description:
      'Draft entire gameplay loops, balance mechanics, and produce assets with our AI toolkit.',
  },
  {
    icon: <FiUsers className="text-primary text-3xl" />,
    title: 'Collaborative Workspaces',
    description:
      'Invite teammates, co-design in real time, and keep your production pipeline in sync.',
  },
  {
    icon: <FiZap className="text-primary text-3xl" />,
    title: 'Lightning Deployments',
    description:
      'Push builds instantly to the Vibe Arcade and gather playtest feedback in minutes.',
  },
  {
    icon: <FiShield className="text-primary text-3xl" />,
    title: 'Secure Distribution',
    description:
      'Ship confidently with role-based access, encrypted assets, and automated QA checks.',
  },
];

const testimonials = [
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
];

const trendingGames = [
  {
    title: 'Neon Skyline',
    genre: 'Cyberpunk Strategy',
    blurb: 'Tactile city building meets noir storytelling in this player-driven metropolis sim.',
  },
  {
    title: 'Echo Drift',
    genre: 'Rhythm Roguelite',
    blurb: 'Battle distorted echoes with synced combat moves and AI-generated soundscapes.',
  },
  {
    title: 'Starloom',
    genre: 'Co-op Crafting',
    blurb: 'Warp between biomes, stitch resources, and craft artifacts that reshape the cosmos.',
  },
];

const HomePage = () => (
  <div className="space-y-20 pb-20">
    <section className="pt-20 text-center space-y-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <span className="px-4 py-1 bg-primary/10 text-primary rounded-full text-sm font-semibold">
          Vibe Coding AI Platform
        </span>
        <h1 className="text-4xl md:text-6xl font-extrabold leading-tight">
          Build, test, and launch unforgettable games with an AI-first workflow.
        </h1>
        <p className="text-gray-300 text-lg">
          From ideation to live operations, Vibe Coding AI equips studios with collaborative editors,
          automated asset generation, and actionable analytics.
        </p>
        <div className="flex justify-center space-x-4">
          <Link
            to="/create"
            className="px-6 py-3 bg-primary hover:bg-secondary transition-colors rounded-lg font-semibold"
          >
            Launch Creator Dashboard
          </Link>
          <Link
            to="/signup"
            className="px-6 py-3 border border-primary/50 hover:border-secondary transition-colors rounded-lg font-semibold"
          >
            Request Studio Access
          </Link>
        </div>
      </div>
    </section>

    <section className="max-w-6xl mx-auto px-6">
      <h2 className="text-3xl font-bold mb-10">Why studios choose Vibe Coding AI</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        {features.map((feature) => (
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
            <div key={game.title} className="bg-dark border border-gray-800 rounded-xl p-6 space-y-3">
              <h3 className="text-2xl font-semibold">{game.title}</h3>
              <span className="inline-block text-sm text-primary font-semibold">{game.genre}</span>
              <p className="text-gray-400 text-sm leading-relaxed">{game.blurb}</p>
            </div>
          ))}
        </div>
      </div>
    </section>

    <section className="max-w-5xl mx-auto px-6 text-center space-y-8">
      <h2 className="text-3xl font-bold">Studios scaling with Vibe</h2>
      <div className="grid md:grid-cols-3 gap-6">
        {testimonials.map((item) => (
          <blockquote
            key={item.author}
            className="bg-dark-800 border border-gray-800 rounded-xl p-6 space-y-4"
          >
            <p className="text-gray-200 italic">{item.quote}</p>
            <footer className="text-gray-400 text-sm">{item.author}</footer>
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

export default HomePage;
