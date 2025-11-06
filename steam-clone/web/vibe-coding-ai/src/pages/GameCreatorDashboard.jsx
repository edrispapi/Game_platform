import { useState } from 'react';
import {
  FiSettings,
  FiShare2,
  FiPlay,
  FiImage,
  FiDownload,
  FiCode,
  FiLayers,
  FiTrendingUp,
  FiCopy,
} from 'react-icons/fi';

const editorTabs = ['Overview', 'Scene Editor', 'Logic Blocks', 'AI Prompts'];
const assets = [
  { name: 'Cyber City Skybox', type: 'Environment', size: '24 MB' },
  { name: 'Synthwave Boss Theme', type: 'Audio', size: '8 MB' },
  { name: 'Neon Racer', type: 'Character', size: '12 MB' },
  { name: 'Drift Particles', type: 'VFX', size: '2 MB' },
];

const sharingOptions = [
  { label: 'Copy shareable link', action: 'link', description: 'Invite others to playtest in the browser.' },
  { label: 'Generate embed snippet', action: 'embed', description: 'Drop the build into your marketing site.' },
  { label: 'Publish to marketplace', action: 'market', description: 'Ship to the Vibe Arcade for monetization.' },
];

const GameCreatorDashboard = () => {
  const [activeTab, setActiveTab] = useState('Overview');
  const [isSharing, setIsSharing] = useState(false);
  const [selectedSettings, setSelectedSettings] = useState({
    difficulty: 'Adaptive',
    monetization: true,
    telemetry: true,
    nightlyBuilds: false,
  });

  return (
    <div className="container mx-auto px-6 py-12 space-y-10">
      <header className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div>
          <p className="text-sm text-primary uppercase tracking-[0.3em]">Build: NEON-ALPHA-07</p>
          <h1 className="text-4xl font-bold mt-2">Game Creator Dashboard</h1>
          <p className="text-gray-400 mt-3 max-w-2xl">
            Manage your project, tweak AI systems, and collaborate with your team without leaving the cockpit.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button className="px-5 py-2 rounded-lg border border-primary text-primary hover:bg-primary/10 font-semibold transition">
            <FiDownload className="mr-2" /> Export build
          </button>
          <button
            onClick={() => setIsSharing(true)}
            className="px-5 py-2 rounded-lg bg-primary hover:bg-secondary text-white font-semibold transition inline-flex items-center gap-2"
          >
            <FiShare2 /> Share prototype
          </button>
        </div>
      </header>

      <section className="bg-dark-800 border border-gray-800 rounded-2xl">
        <div className="flex flex-wrap border-b border-gray-800">
          {editorTabs.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-3 text-sm font-medium transition border-b-2 ${
                activeTab === tab ? 'text-primary border-primary' : 'text-gray-400 border-transparent hover:text-primary'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
        <div className="p-6 space-y-6">
          {activeTab === 'Overview' && (
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-4">
                <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-semibold">Milestone progress</h2>
                    <span className="text-xs px-3 py-1 rounded-full bg-primary/20 text-primary">Sprint 18</span>
                  </div>
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Core gameplay loop</p>
                      <div className="w-full bg-gray-800 h-2 rounded-full">
                        <div className="h-full bg-primary rounded-full" style={{ width: '82%' }} />
                      </div>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400 mb-1">AI persona scripting</p>
                      <div className="w-full bg-gray-800 h-2 rounded-full">
                        <div className="h-full bg-secondary rounded-full" style={{ width: '67%' }} />
                      </div>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Multiplayer sync</p>
                      <div className="w-full bg-gray-800 h-2 rounded-full">
                        <div className="h-full bg-primary/70 rounded-full" style={{ width: '54%' }} />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
                  <h2 className="text-xl font-semibold flex items-center gap-2">
                    <FiTrendingUp className="text-primary" />
                    Playtest insights
                  </h2>
                  <ul className="space-y-3 text-sm text-gray-400">
                    <li>• Average session length increased 12% after the new dynamic difficulty update.</li>
                    <li>• 67% of players favored the “Nightfall” track variation during weekend runs.</li>
                    <li>• AI commentary module boosted social sharing by 22% in the last sprint.</li>
                  </ul>
                </div>
              </div>
              <div className="space-y-4">
                <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
                  <h2 className="text-xl font-semibold flex items-center gap-2">
                    <FiLayers className="text-primary" />
                    Build channels
                  </h2>
                  <div className="space-y-3 text-sm text-gray-400">
                    <p>
                      <span className="font-semibold text-gray-200">QA Arena:</span> nightly stress tests with automation bots
                    </p>
                    <p>
                      <span className="font-semibold text-gray-200">Creator Labs:</span> community modding sandbox
                    </p>
                    <p>
                      <span className="font-semibold text-gray-200">Investor Deck:</span> curated highlight reel
                    </p>
                  </div>
                </div>
                <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 space-y-4">
                  <h2 className="text-xl font-semibold flex items-center gap-2">
                    <FiCode className="text-primary" />
                    Latest AI prompt
                  </h2>
                  <p className="text-sm text-gray-400 bg-dark-800 border border-gray-800 rounded-lg p-4">
                    “Design a rival racer with adaptive taunts reacting to player drift accuracy. Tone should be playful but
                    competitive. Include unique synthwave-inspired voice filters.”
                  </p>
                  <button className="text-primary hover:text-secondary text-sm inline-flex items-center gap-2">
                    <FiCopy /> Copy prompt
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'Scene Editor' && (
            <div className="grid lg:grid-cols-[2fr,1fr] gap-6">
              <div className="bg-gray-900 rounded-xl border border-gray-800 h-80 flex items-center justify-center">
                <p className="text-gray-400 max-w-md text-center">
                  Scene preview updates live as you adjust atmosphere, lighting, and AI agent behaviors.
                </p>
              </div>
              <div className="space-y-4">
                <div className="bg-gray-900 rounded-xl border border-gray-800 p-5 space-y-3">
                  <h3 className="text-lg font-semibold">Environment presets</h3>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    {['Neon City', 'Twilight Docks', 'Stellar Freeway', 'Duststorm Outlands'].map((preset) => (
                      <button key={preset} className="px-3 py-2 rounded-lg bg-dark-800 border border-gray-800 hover:border-primary">
                        {preset}
                      </button>
                    ))}
                  </div>
                </div>
                <div className="bg-gray-900 rounded-xl border border-gray-800 p-5 space-y-3">
                  <h3 className="text-lg font-semibold">Atmosphere controls</h3>
                  <div className="space-y-2 text-sm text-gray-400">
                    <p>Fog density <span className="float-right text-gray-200">31%</span></p>
                    <p>Neon glow <span className="float-right text-gray-200">68%</span></p>
                    <p>Traffic AI activity <span className="float-right text-gray-200">High</span></p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'Logic Blocks' && (
            <div className="grid lg:grid-cols-[3fr,2fr] gap-6">
              <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Event flow</h3>
                  <button className="text-sm text-primary hover:text-secondary inline-flex items-center gap-2">
                    <FiCopy /> Duplicate flow
                  </button>
                </div>
                <div className="grid gap-4">
                  {['Countdown', 'Race Loop', 'Dynamic Rival', 'Reward Ceremony'].map((block) => (
                    <div key={block} className="p-4 rounded-xl bg-dark-800 border border-gray-800">
                      <p className="font-semibold text-gray-200">{block}</p>
                      <p className="text-sm text-gray-400 mt-1">
                        Drag AI behaviors, audio cues, and VFX triggers to customize how the sequence unfolds.
                      </p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 space-y-4">
                <h3 className="text-lg font-semibold">Smart suggestions</h3>
                <ul className="space-y-3 text-sm text-gray-400">
                  <li>• Add a “boost leak” event when players draft behind rivals for longer than 5 seconds.</li>
                  <li>• Introduce crowd reactions that react to AI taunts for heightened immersion.</li>
                  <li>• Offer weekly tournaments with rotating modifiers for retention.</li>
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'AI Prompts' && (
            <div className="grid lg:grid-cols-2 gap-6">
              <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 space-y-4">
                <h3 className="text-lg font-semibold">Prompt history</h3>
                <ul className="space-y-3 text-sm text-gray-400">
                  <li>
                    <span className="text-gray-200">Dialogue remix:</span> “Inject humor when players recover from a crash without
                    activating rewind.”
                  </li>
                  <li>
                    <span className="text-gray-200">Environment flair:</span> “Blend aurora particles during midnight rain sequences.”
                  </li>
                  <li>
                    <span className="text-gray-200">Boss behavior:</span> “Escalate aggression if the player maintains top speed for 60 seconds.”
                  </li>
                </ul>
              </div>
              <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 space-y-4">
                <h3 className="text-lg font-semibold">Compose new prompt</h3>
                <textarea
                  rows={6}
                  placeholder="Describe the persona, mechanics, or ambience you want the AI to generate."
                  className="w-full rounded-xl bg-dark-800 border border-gray-800 focus:border-primary focus:ring-1 focus:ring-primary px-4 py-3 text-sm"
                />
                <button className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary hover:bg-secondary text-white font-semibold transition">
                  <FiPlay /> Generate
                </button>
              </div>
            </div>
          )}
        </div>
      </section>

      <section className="grid lg:grid-cols-[2fr,1fr] gap-6">
        <div className="bg-dark-800 border border-gray-800 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <FiImage className="text-primary" /> Asset library
            </h2>
            <button className="text-sm text-primary hover:text-secondary">Upload asset</button>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            {assets.map((asset) => (
              <div key={asset.name} className="bg-gray-900 rounded-xl border border-gray-800 p-4">
                <p className="font-semibold text-gray-200">{asset.name}</p>
                <p className="text-sm text-gray-400">{asset.type}</p>
                <p className="text-xs text-gray-500 mt-2">{asset.size}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-dark-800 border border-gray-800 rounded-2xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <FiSettings className="text-primary" /> Build settings
            </h2>
            <button className="text-sm text-primary hover:text-secondary">Edit defaults</button>
          </div>
          <div className="space-y-3 text-sm text-gray-400">
            <label className="flex items-center justify-between">
              <span>Difficulty</span>
              <select
                value={selectedSettings.difficulty}
                onChange={(event) =>
                  setSelectedSettings((prev) => ({ ...prev, difficulty: event.target.value }))
                }
                className="bg-dark-800 border border-gray-800 rounded-lg px-3 py-2 text-sm focus:border-primary focus:outline-none"
              >
                <option value="Adaptive">Adaptive</option>
                <option value="Competitive">Competitive</option>
                <option value="Story">Story</option>
              </select>
            </label>
            <label className="flex items-center justify-between">
              <span>Monetization hooks</span>
              <input
                type="checkbox"
                checked={selectedSettings.monetization}
                onChange={(event) =>
                  setSelectedSettings((prev) => ({ ...prev, monetization: event.target.checked }))
                }
                className="form-checkbox h-4 w-4 text-primary"
              />
            </label>
            <label className="flex items-center justify-between">
              <span>Telemetry insights</span>
              <input
                type="checkbox"
                checked={selectedSettings.telemetry}
                onChange={(event) =>
                  setSelectedSettings((prev) => ({ ...prev, telemetry: event.target.checked }))
                }
                className="form-checkbox h-4 w-4 text-primary"
              />
            </label>
            <label className="flex items-center justify-between">
              <span>Nightly builds</span>
              <input
                type="checkbox"
                checked={selectedSettings.nightlyBuilds}
                onChange={(event) =>
                  setSelectedSettings((prev) => ({ ...prev, nightlyBuilds: event.target.checked }))
                }
                className="form-checkbox h-4 w-4 text-primary"
              />
            </label>
          </div>
        </div>
      </section>

      {isSharing && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-6 z-50">
          <div className="bg-dark-800 border border-gray-800 rounded-3xl p-8 max-w-xl w-full space-y-6">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-2xl font-semibold">Share your prototype</h2>
                <p className="text-gray-400 mt-1">
                  Send a playable build or embed the experience anywhere. Choose how you want to collaborate.
                </p>
              </div>
              <button onClick={() => setIsSharing(false)} className="text-gray-400 hover:text-primary">
                ✕
              </button>
            </div>
            <div className="space-y-4">
              {sharingOptions.map((option) => (
                <button
                  key={option.action}
                  className="w-full text-left bg-gray-900 border border-gray-800 hover:border-primary rounded-2xl px-5 py-4"
                >
                  <p className="font-semibold text-gray-200">{option.label}</p>
                  <p className="text-sm text-gray-400">{option.description}</p>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameCreatorDashboard;
