import AuthForm from '../components/AuthForm';

const SignUpPage = () => (
  <div className="container mx-auto px-6 py-20">
    <div className="max-w-3xl mx-auto text-center mb-12">
      <h1 className="text-3xl font-bold mb-3">Create your Vibe Coding AI account</h1>
      <p className="text-gray-400">
        Start your 14-day pilot and unlock AI-assisted creation, automated QA, and real-time co-op features.
      </p>
    </div>
    <AuthForm type="signup" />
  </div>
);

export default SignUpPage;
