import Link from 'next/link'

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">R</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Renovation Automations</h1>
              <p className="text-sm text-gray-500">Demo Portal</p>
            </div>
          </Link>
          
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/" className="text-gray-600 hover:text-primary-600 transition-colors">
              Browse Demos
            </Link>
            <Link href="/my-demos" className="text-gray-600 hover:text-primary-600 transition-colors">
              My Demos
            </Link>
            <Link href="/support" className="text-gray-600 hover:text-primary-600 transition-colors">
              Support
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
