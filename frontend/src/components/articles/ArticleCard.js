import React from 'react';
import { Avatar } from 'primereact/avatar';
import { Link } from 'react-router-dom';

const ArticleCard = ({ article }) => {
  return (
    <div className="shadow-2 border-round h-full surface-card">
      <Link to={'/articles/' + article.id} className="no-underline text-900 hover:text-700">
        <img src={article.image} alt={article.title} className="block w-full border-round-top" />
        <div className="p-4">
          <span className={`block font-medium text-${article.categoryColor} mb-3`}>{article.category}</span>
          <div className="text-xl font-medium mb-3 line-height-3">{article.title}</div>
          <div className="line-height-3 mb-3 text-700">{article.excerpt}</div>
          <div className="flex">
            <Avatar image={article.author.avatar} shape="circle" size="large" />
            <div className="ml-2">
              <div className="text-sm font-bold text-900 mb-1">{article.author.name}</div>
              <div className="text-sm flex align-items-center text-700">
                <i className="pi pi-calendar mr-1 text-sm"></i>
                <span>{article.date}</span>
              </div>
            </div>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default ArticleCard;
