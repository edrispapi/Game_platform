import AuthForm from '../components/AuthForm';

const LoginPage = () => (
  <div className="max-w-4xl mx-auto py-20 px-6 space-y-6 text-center">
    <div>
      <h1 className="text-3xl font-bold">Sign in to Vibe Coding AI</h1>
      <p className="text-gray-400">
        Access your studio dashboards, AI pipelines, and analytics from one secure workspace.
      </p>
    </div>
    <AuthForm type="login" />
  </div>
);

export default LoginPage;
