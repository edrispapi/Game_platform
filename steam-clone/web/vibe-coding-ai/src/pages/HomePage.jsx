import { Link } from 'react-router-dom';
import { FiPlayCircle, FiUsers, FiAward, FiTrendingUp, FiArrowRight } from 'react-icons/fi';

const features = [
  {
    icon: <FiPlayCircle className="text-primary text-3xl" />,
    title: 'Instant Game Generation',
    description: 'Transform your ideas into playable prototypes with AI-assisted scene and mechanic builders.',
  },
  {
    icon: <FiUsers className="text-primary text-3xl" />,
    title: 'Collaborative Workflows',
    description: 'Invite teammates to co-create worlds, scripts, and art assets in real time.',
  },
  {
    icon: <FiTrendingUp className="text-primary text-3xl" />,
    title: 'Player Analytics',
    description: 'Optimize retention with built-in heatmaps, funnels, and live feedback dashboards.',
  },
];

const trendingGames = [
  {
    title: 'Neon Drift Legends',
    genre: 'Cyberpunk Racer',
    players: '12.4k active',
    description: 'Race through procedurally generated megacities tuned by ML-driven difficulty scaling.',
  },
  {
    title: 'Mythos Tactics',
    genre: 'Turn-Based Strategy',
    players: '9.1k active',
    description: 'Craft squads of AI-authored heroes and challenge community campaigns.',
  },
  {
    title: 'Synthwave Odyssey',
    genre: 'Story Adventure',
    players: '7.8k active',
    description: 'Narratives adapt dynamically to player emotion signals for a personalized arc.',
  },
];

const testimonials = [
  {
    name: 'Aria Thompson',
    role: 'Indie Narrative Designer',
    quote:
      'Vibe Coding AI helped me script branching storylines in days instead of weeks. The AI prompts are spot on.',
  },
  {
    name: 'Jalen Park',
    role: 'Studio Technical Director',
    quote: 'The asset pipelines plug straight into our CI. Our prototyping speed tripled after migrating.',
  },
  {
    name: 'Sofia Ahmed',
    role: 'Community Creator',
    quote: 'Collaborating with my audience in real time keeps our games fresh. The platform feels premium.',
  },
];

const HomePage = () => (
  <div className="space-y-20 pb-20">
    <section className="relative overflow-hidden bg-gradient-to-b from-dark via-dark-800 to-dark">
      <div className="container mx-auto px-6 py-24 flex flex-col lg:flex-row items-center gap-16">
        <div className="max-w-2xl space-y-6">
          <span className="inline-flex items-center px-4 py-1 rounded-full border border-primary/40 text-primary text-sm uppercase tracking-widest">
            Next-gen creation suite
          </span>
          <h1 className="text-4xl lg:text-6xl font-extrabold leading-tight">
            Build immersive game experiences with <span className="text-primary">AI superpowers</span>.
          </h1>
          <p className="text-gray-300 text-lg">
            Orchestrate game design, asset generation, testing, and publishing from a single command center. Tailored
            for ambitious studios and indie dreamers alike.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link
              to="/create"
              className="px-6 py-3 rounded-lg bg-primary hover:bg-secondary text-white font-semibold inline-flex items-center gap-2 transition"
            >
              Launch creator
              <FiArrowRight />
            </Link>
            <Link
              to="/signup"
              className="px-6 py-3 rounded-lg border border-primary text-primary hover:bg-primary/10 font-semibold transition"
            >
              Start free trial
            </Link>
          </div>
          <div className="flex items-center gap-6 text-sm text-gray-400">
            <div className="flex items-center gap-2">
              <FiAward className="text-primary" />
              Voted #1 AI game builder 2025
            </div>
            <div className="flex items-center gap-2">
              <FiUsers className="text-primary" />
              Trusted by 40k+ creators
            </div>
          </div>
        </div>
        <div className="relative w-full max-w-xl">
          <div className="absolute inset-0 bg-primary/20 blur-3xl rounded-full" />
          <div className="relative bg-dark-800 border border-gray-800 rounded-3xl p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Live project snapshot</span>
              <span className="text-xs px-3 py-1 bg-primary/20 text-primary rounded-full">AI enhanced</span>
            </div>
            <div className="bg-gray-900 rounded-2xl h-48 flex items-center justify-center">
              <p className="text-gray-400 text-center max-w-sm">
                Visualize adaptive lighting, procedural terrains, and dynamic NPC scripts before deployment.
              </p>
            </div>
            <div className="grid grid-cols-3 gap-3 text-sm">
              <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800 text-gray-300">
                <p className="text-xs text-gray-500">Build status</p>
                <p className="font-semibold text-primary">Stable</p>
              </div>
              <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800 text-gray-300">
                <p className="text-xs text-gray-500">AI prompts</p>
                <p className="font-semibold">132 synced</p>
              </div>
              <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800 text-gray-300">
                <p className="text-xs text-gray-500">Player cohort</p>
                <p className="font-semibold">Beta Wave 02</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section className="container mx-auto px-6">
      <div className="grid md:grid-cols-3 gap-6">
        {features.map((feature) => (
          <div key={feature.title} className="bg-dark-800 border border-gray-800 rounded-2xl p-8 space-y-4">
            {feature.icon}
            <h3 className="text-xl font-semibold">{feature.title}</h3>
            <p className="text-gray-400">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>

    <section className="container mx-auto px-6 space-y-10">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold">Trending community launches</h2>
          <p className="text-gray-400">Curated weekly from thousands of playtests.</p>
        </div>
        <Link to="/games" className="text-primary hover:text-secondary inline-flex items-center gap-2">
          Explore all <FiArrowRight />
        </Link>
      </div>
      <div className="grid lg:grid-cols-3 gap-6">
        {trendingGames.map((game) => (
          <article key={game.title} className="bg-dark-800 border border-gray-800 rounded-2xl p-6 space-y-3">
            <div className="flex items-center justify-between text-sm text-gray-400">
              <span>{game.genre}</span>
              <span>{game.players}</span>
            </div>
            <h3 className="text-2xl font-semibold">{game.title}</h3>
            <p className="text-gray-400 text-sm">{game.description}</p>
            <button className="mt-2 inline-flex items-center gap-2 text-primary hover:text-secondary text-sm font-medium">
              View case study <FiArrowRight />
            </button>
          </article>
        ))}
      </div>
    </section>

    <section className="container mx-auto px-6">
      <div className="bg-dark-800 border border-gray-800 rounded-3xl px-8 py-12 grid md:grid-cols-3 gap-8">
        {testimonials.map((testimonial) => (
          <div key={testimonial.name} className="space-y-4">
            <p className="text-gray-300 text-lg">“{testimonial.quote}”</p>
            <div>
              <p className="font-semibold">{testimonial.name}</p>
              <p className="text-sm text-gray-500">{testimonial.role}</p>
            </div>
          </div>
        ))}
      </div>
    </section>

    <section className="container mx-auto px-6">
      <div className="bg-gradient-to-r from-primary/20 via-secondary/10 to-primary/20 border border-primary/40 rounded-3xl px-10 py-12 flex flex-col lg:flex-row items-center justify-between gap-8">
        <div className="space-y-4 max-w-xl">
          <h2 className="text-3xl font-bold">Launch your next playable in record time.</h2>
          <p className="text-gray-200">
            Join elite creators and enterprises scaling with AI-driven workflows. Get full access to the Vibe Coding AI
            toolbox, or integrate it with your existing stack via our SDKs.
          </p>
        </div>
        <div className="flex flex-col sm:flex-row gap-4">
          <Link to="/signup" className="px-6 py-3 rounded-lg bg-primary hover:bg-secondary text-white font-semibold transition">
            Claim early access
          </Link>
          <Link
            to="/contact"
            className="px-6 py-3 rounded-lg border border-primary text-primary hover:bg-primary/10 font-semibold transition"
          >
            Talk to sales
          </Link>
        </div>
      </div>
    </section>
  </div>
);

export default HomePage;
