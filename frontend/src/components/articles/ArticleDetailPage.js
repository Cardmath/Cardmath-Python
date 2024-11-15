import React from 'react';
import { useParams } from 'react-router-dom'; // Assuming you're using react-router
import { articles } from '../../data/articlesData';
import Navbar from '../Navbar';
import Footer from '../Footer';

const ArticleDetailPage = () => {
    const { id } = useParams();
    const article = articles.find((article) => article.id === parseInt(id));

    if (!article) {
        return <div>Article not found.</div>;
    }

    return (
        <div>
            <Navbar />
            <div className="surface-section px-4 py-8 md:px-6 lg:px-8 text-700">
                <div className="flex flex-wrap">
                    <div className="w-full lg:w-6 pr-0 lg:pr-5">
                        <span
                            className={`text-${article.categoryColor} bg-${article.categoryColor.replace(
                                '600',
                                '50'
                            )} inline-block py-2 px-3`}
                            style={{ borderRadius: '50px' }}
                        >
                            {article.category}
                        </span>
                        <div className="font-normal text-2xl mt-3 mb-3 text-900">{article.title}</div>
                        <div className="text-600 mb-5">
                            by {article.author.name} | {article.author.website || 'website.com'} | {article.readTime}
                        </div>
                        {article.content.split('\n\n').map((paragraph, idx) => (
                            <p key={idx} className={`line-height-3 ${idx !== 0 ? 'mt-0 mb-5' : ''}`}>
                                {paragraph}
                            </p>
                        ))}
                    </div>
                    <div className="w-full lg:w-6 pl-0 lg:pl-5 pt-5">
                        <img src={article.image} alt={article.title} className="w-full border-round" />
                        <div className="text-center text-sm font-medium mt-3">{article.imageCaption}</div>
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default ArticleDetailPage;
