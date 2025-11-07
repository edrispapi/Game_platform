import AuthForm from '../components/AuthForm';

const SignUpPage = () => (
  <div className="max-w-4xl mx-auto py-20 px-6 space-y-6 text-center">
    <div>
      <h1 className="text-3xl font-bold">Create your studio account</h1>
      <p className="text-gray-400">
        Unlock AI co-creation tools, asset generation pipelines, and collaborative workspaces for your team.
      </p>
    </div>
    <AuthForm type="signup" />
  </div>
);

export default SignUpPage;
