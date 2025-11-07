import { useMemo, useState } from 'react';
import {
  FiActivity,
  FiBarChart2,
  FiCode,
  FiEdit3,
  FiImage,
  FiLink,
  FiSettings,
  FiShare2,
  FiUploadCloud,
} from 'react-icons/fi';

const TabButton = ({ active, icon: Icon, label, onClick }) => (
  <button
    type="button"
    onClick={onClick}
    className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
      active
        ? 'bg-primary text-white border-primary'
        : 'bg-dark-800 border-gray-800 hover:border-primary/60'
    }`}
  >
    <Icon />
    <span>{label}</span>
  </button>
);

const EditorPane = ({ script, onScriptChange }) => (
  <div className="space-y-4">
    <h3 className="text-lg font-semibold flex items-center space-x-2">
      <FiCode />
      <span>Gameplay Script</span>
    </h3>
    <textarea
      value={script}
      onChange={(event) => onScriptChange(event.target.value)}
      rows={16}
      className="w-full bg-dark-800 border border-gray-800 rounded-lg p-4 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-primary"
    />
    <button className="inline-flex items-center space-x-2 px-4 py-2 bg-primary hover:bg-secondary transition-colors rounded-lg font-semibold">
      <FiUploadCloud />
      <span>Commit to workspace</span>
    </button>
  </div>
);

const PreviewPane = ({ buildStatus }) => (
  <div className="space-y-6">
    <h3 className="text-lg font-semibold flex items-center space-x-2">
      <FiActivity />
      <span>Live Preview</span>
    </h3>
    <div className="aspect-video bg-dark-800 border border-gray-800 rounded-xl flex items-center justify-center">
      <p className="text-gray-500">Preview canvas ready for your next build.</p>
    </div>
    <div className="bg-dark-800 border border-gray-800 rounded-xl p-4 space-y-2">
      <div className="flex items-center justify-between">
        <span className="font-medium text-gray-300">Latest Build</span>
        <span className="text-sm text-gray-400">{buildStatus.version}</span>
      </div>
      <p className="text-sm text-gray-400">Status: {buildStatus.state}</p>
      <p className="text-sm text-gray-500">Triggered: {buildStatus.timestamp}</p>
    </div>
  </div>
);

const AssetPane = ({ assets }) => (
  <div className="space-y-6">
    <div className="flex items-center justify-between">
      <h3 className="text-lg font-semibold flex items-center space-x-2">
        <FiImage />
        <span>Asset Library</span>
      </h3>
      <button className="inline-flex items-center space-x-2 px-4 py-2 bg-primary hover:bg-secondary transition-colors rounded-lg font-semibold">
        <FiUploadCloud />
        <span>Upload asset</span>
      </button>
    </div>
    <div className="grid md:grid-cols-2 gap-4">
      {assets.map((asset) => (
        <div key={asset.name} className="bg-dark-800 border border-gray-800 rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-semibold">{asset.name}</h4>
              <p className="text-xs text-gray-400">{asset.type}</p>
            </div>
            <span className="text-xs text-gray-500">{asset.size}</span>
          </div>
          <p className="text-sm text-gray-400">Updated {asset.updated}</p>
        </div>
      ))}
    </div>
  </div>
);

const SharePane = ({ shareLinks }) => (
  <div className="space-y-6">
    <h3 className="text-lg font-semibold flex items-center space-x-2">
      <FiShare2 />
      <span>Distribute Builds</span>
    </h3>
    <div className="grid md:grid-cols-2 gap-4">
      {shareLinks.map((link) => (
        <div key={link.label} className="bg-dark-800 border border-gray-800 rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between">
            <span className="font-medium">{link.label}</span>
            <span className="text-xs text-primary">{link.access}</span>
          </div>
          <p className="text-sm text-gray-400 break-all">{link.url}</p>
          <button className="w-full px-3 py-2 border border-primary/60 hover:border-secondary transition-colors rounded-lg text-sm font-semibold">
            Copy link
          </button>
        </div>
      ))}
    </div>
  </div>
);

const SettingsPane = () => (
  <div className="grid md:grid-cols-2 gap-6">
    <div className="bg-dark-800 border border-gray-800 rounded-xl p-6 space-y-4">
      <h3 className="text-lg font-semibold flex items-center space-x-2">
        <FiSettings />
        <span>Project Settings</span>
      </h3>
      <label className="text-sm text-gray-400">Game Title</label>
      <input
        type="text"
        defaultValue="Project Nebula"
        className="w-full bg-dark border border-gray-800 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
      />
      <label className="text-sm text-gray-400">Team Visibility</label>
      <select className="w-full bg-dark border border-gray-800 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary">
        <option>Studio Wide</option>
        <option>Core Team</option>
        <option>Invite Only</option>
      </select>
    </div>
    <div className="bg-dark-800 border border-gray-800 rounded-xl p-6 space-y-4">
      <h3 className="text-lg font-semibold flex items-center space-x-2">
        <FiBarChart2 />
        <span>Analytics Digest</span>
      </h3>
      <p className="text-sm text-gray-400">
        Monitor player retention, monetization funnels, and build health directly inside the dashboard.
        Configure automated alerts to stay ahead of regressions.
      </p>
      <button className="inline-flex items-center space-x-2 px-4 py-2 border border-primary/60 hover:border-secondary transition-colors rounded-lg font-semibold">
        View detailed report
      </button>
    </div>
  </div>
);

const tabs = [
  { id: 'editor', label: 'Editor', icon: FiEdit3 },
  { id: 'preview', label: 'Preview', icon: FiActivity },
  { id: 'assets', label: 'Assets', icon: FiImage },
  { id: 'share', label: 'Share', icon: FiShare2 },
  { id: 'settings', label: 'Settings', icon: FiSettings },
];

const GameCreatorDashboard = () => {
  const [activeTab, setActiveTab] = useState('editor');
  const [script, setScript] = useState(`// AI generated gameplay scaffold\nfunction initLevel() {\n  spawnPlayer({ x: 12, y: 6 });\n  spawnEnemyWave({ count: 8, pattern: 'spiral' });\n}\n`);

  const buildStatus = useMemo(
    () => ({
      version: 'v0.5.2-beta',
      state: 'Ready for QA',
      timestamp: '12 minutes ago',
    }),
    []
  );

  const assets = useMemo(
    () => [
      { name: 'Neon_Runner.fbx', type: 'Character Rig', size: '4.2 MB', updated: '2 hours ago' },
      { name: 'Skyline_Layered.psd', type: 'Environment Art', size: '68 MB', updated: 'yesterday' },
      { name: 'Pulse_Combat.wav', type: 'Audio Loop', size: '12 MB', updated: '3 days ago' },
      { name: 'Control_Schemes.json', type: 'Input Mapping', size: '8 KB', updated: '5 days ago' },
    ],
    []
  );

  const shareLinks = useMemo(
    () => [
      {
        label: 'Stakeholder Build',
        access: 'Password protected',
        url: 'https://vibecoding.ai/builds/neon/qa',
      },
      {
        label: 'Playtester Cohort',
        access: 'Invite only',
        url: 'https://vibecoding.ai/builds/neon/playtest',
      },
      {
        label: 'Internal Sandbox',
        access: 'Studio network',
        url: 'https://vibecoding.ai/builds/neon/internal',
      },
      {
        label: 'Marketing Preview',
        access: 'Public preview',
        url: 'https://vibecoding.ai/builds/neon/trailer',
      },
    ],
    []
  );

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      <header className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
        <div>
          <h1 className="text-3xl font-bold">Creator Dashboard</h1>
          <p className="text-gray-400">
            Manage your AI-assisted workflows, assets, and deployment pipelines from a single command center.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button className="px-4 py-2 border border-primary/60 hover:border-secondary transition-colors rounded-lg font-semibold">
            View release notes
          </button>
          <button className="inline-flex items-center space-x-2 px-4 py-2 bg-primary hover:bg-secondary transition-colors rounded-lg font-semibold">
            <FiLink />
            <span>Connect integrations</span>
          </button>
        </div>
      </header>

      <div className="flex flex-wrap gap-3">
        {tabs.map((tab) => (
          <TabButton
            key={tab.id}
            icon={tab.icon}
            label={tab.label}
            active={tab.id === activeTab}
            onClick={() => setActiveTab(tab.id)}
          />
        ))}
      </div>

      <section className="bg-dark border border-gray-800 rounded-xl p-6">
        {activeTab === 'editor' && (
          <EditorPane script={script} onScriptChange={setScript} />
        )}
        {activeTab === 'preview' && <PreviewPane buildStatus={buildStatus} />}
        {activeTab === 'assets' && <AssetPane assets={assets} />}
        {activeTab === 'share' && <SharePane shareLinks={shareLinks} />}
        {activeTab === 'settings' && <SettingsPane />}
      </section>
    </div>
  );
};

export default GameCreatorDashboard;
