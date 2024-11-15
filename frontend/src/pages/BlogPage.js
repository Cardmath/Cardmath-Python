import React from 'react';
import { articles } from '../data/articlesData';
import ArticleCard from '../components/articles/ArticleCard';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const BlogPage = () => {
  return (
    <div> 
        <Navbar />
        <div className="surface-section px-4 py-8 md:px-6 lg:px-8">
        <div className="font-bold text-5xl text-900 mb-5 text-center">Featured Articles</div>
        <div className="grid nogutter">
            {articles.map((article) => (
            <div key={article.id} className="col-12 lg:col-4 p-3">
                <ArticleCard article={article} />
            </div>
            ))}
        </div>
        </div>
        <Footer />
    </div>
  );
};

export default BlogPage;
