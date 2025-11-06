import AuthForm from '../components/AuthForm';

const LoginPage = () => (
  <div className="container mx-auto px-6 py-20">
    <div className="max-w-3xl mx-auto text-center mb-12">
      <h1 className="text-3xl font-bold mb-3">Access your creator cockpit</h1>
      <p className="text-gray-400">
        Log in to continue iterating on your in-flight builds, review analytics, and collaborate with your team.
      </p>
    </div>
    <AuthForm type="login" />
  </div>
);

export default LoginPage;
