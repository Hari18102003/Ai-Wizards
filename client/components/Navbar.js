import Link from 'next/link'
import React from 'react'

const Navbar = () => {
    return (
        <nav className="w-full p-6 shadow-md">
            <Link href={'/'}><h1 className="text-4xl font-bold bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 bg-clip-text text-transparent inline-block">
                Textify.AI
            </h1></Link>
        </nav>

    )
}

export default Navbar