-- Simple MySQL Database Setup Script for Sarbottam Cement Limited
-- Compatible with most MySQL versions

-- Create database
CREATE DATABASE IF NOT EXISTS sarbottam_cement_db;
USE sarbottam_cement_db;

-- Set charset
ALTER DATABASE sarbottam_cement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Company table
CREATE TABLE IF NOT EXISTS sarbottam_company (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL DEFAULT 'Sarbottam Cement Limited',
    symbol VARCHAR(10) NOT NULL DEFAULT 'SARBTM',
    sector VARCHAR(100) NOT NULL DEFAULT 'Manufacturing and Processing',
    founded_year INT NULL,
    headquarters VARCHAR(200) NOT NULL DEFAULT 'Sunwal, Nawalparasi, State-5, Nepal',
    company_type VARCHAR(50) NOT NULL DEFAULT 'Public Company',
    employees VARCHAR(50) NOT NULL DEFAULT '501-1,000 employees',
    description TEXT NOT NULL,
    website VARCHAR(200) NOT NULL DEFAULT 'https://sarbottamcement.com.np',
    email VARCHAR(254) NULL,
    phone VARCHAR(50) NULL,
    market_price DECIMAL(10,2) NULL,
    market_cap VARCHAR(50) NULL,
    pe_ratio DECIMAL(10,2) NULL,
    dividend_yield DECIMAL(5,2) NULL,
    book_value DECIMAL(10,2) NULL,
    roe DECIMAL(5,2) NULL,
    production_capacity VARCHAR(100) NULL,
    annual_revenue VARCHAR(100) NULL,
    net_profit VARCHAR(100) NULL,
    total_assets VARCHAR(100) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Company News table
CREATE TABLE IF NOT EXISTS sarbottam_companynews (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_id BIGINT NOT NULL,
    news_title VARCHAR(300) NOT NULL,
    news_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    news_image VARCHAR(100) NULL,
    news_body TEXT NOT NULL,
    summary TEXT NULL,
    category VARCHAR(100) NULL,
    is_featured TINYINT(1) NOT NULL DEFAULT 0,
    is_published TINYINT(1) NOT NULL DEFAULT 1,
    slug VARCHAR(100) NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id) REFERENCES sarbottam_company(id) ON DELETE CASCADE
);

-- Company Financial data table
CREATE TABLE IF NOT EXISTS sarbottam_companyfinancial (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_id BIGINT NOT NULL,
    report_period VARCHAR(20) NOT NULL,
    total_revenue DECIMAL(15,2) NULL,
    net_income DECIMAL(15,2) NULL,
    earnings_per_share DECIMAL(10,2) NULL,
    total_assets DECIMAL(15,2) NULL,
    total_liabilities DECIMAL(15,2) NULL,
    shareholders_equity DECIMAL(15,2) NULL,
    report_date DATE NOT NULL,
    report_file VARCHAR(100) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id) REFERENCES sarbottam_company(id) ON DELETE CASCADE
);

-- Company Achievements table
CREATE TABLE IF NOT EXISTS sarbottam_companyachievement (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    achievement_date DATE NOT NULL,
    category VARCHAR(100) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id) REFERENCES sarbottam_company(id) ON DELETE CASCADE
);

-- Insert sample company data
INSERT INTO sarbottam_company (
    name, symbol, sector, founded_year, headquarters, company_type, employees,
    description, website, market_price, market_cap, pe_ratio, dividend_yield,
    book_value, roe, production_capacity, annual_revenue, net_profit, total_assets
) VALUES (
    'Sarbottam Cement Limited',
    'SARBTM',
    'Manufacturing and Processing',
    2010,
    'Sunwal, Nawalparasi, State-5, Nepal',
    'Public Company',
    '501-1,000 employees',
    'Sarbottam Cement Limited is an innovator and pioneer of the cement industry of Nepal, being the first and only cement manufacturer to use a completely European production line. The company operates with state-of-the-art technology and sustainable practices.',
    'https://sarbottamcement.com.np',
    265.00,
    '2.12B',
    15.2,
    3.5,
    180.0,
    12.8,
    '500,000 tonnes per year',
    '1.8 billion NPR',
    '180 million NPR',
    '2.5 billion NPR'
);

-- Insert sample news data
INSERT INTO sarbottam_companynews (
    company_id, news_title, news_date, news_body, summary, category, is_featured, is_published, slug
) VALUES
(
    1,
    'Sarbottam Cement Reports Strong Q3 Financial Results with 15% Revenue Growth',
    '2024-07-15 10:00:00',
    'Sarbottam Cement Limited today announced its financial results for the third quarter ended December 2024, reporting a robust 15% year-over-year revenue growth to NPR 450 million. The company\'s strong performance was driven by increased domestic demand for construction materials and successful market penetration strategies.',
    'Sarbottam Cement Limited announced exceptional third-quarter results, showing a 15% increase in revenue compared to the same period last year, driven by increased domestic demand and strategic market expansion.',
    'Financial Results',
    1,
    1,
    'sarbottam-cement-q3-results-2024'
),
(
    1,
    'Sarbottam Cement Launches Environmental Sustainability Initiative',
    '2024-07-02 14:30:00',
    'Sarbottam Cement Limited has launched an ambitious environmental sustainability initiative as part of its commitment to responsible manufacturing and environmental stewardship. The program aims to reduce the company\'s carbon footprint by 25% over the next three years.',
    'The company announces a comprehensive environmental sustainability program aimed at reducing carbon emissions by 25% over the next three years while maintaining production efficiency.',
    'Sustainability',
    1,
    1,
    'sarbottam-cement-sustainability-initiative-2024'
),
(
    1,
    'Board of Directors Approves Dividend Distribution for Shareholders',
    '2024-06-28 11:00:00',
    'The Board of Directors of Sarbottam Cement Limited has approved the distribution of dividend to shareholders at the rate of NPR 12 per share for the fiscal year 2023/24. This represents a significant 20% increase from the previous year\'s dividend of NPR 10 per share.',
    'The Board has approved a dividend payment of NPR 12 per share, representing a 20% increase from the previous year, reflecting the company\'s strong financial performance.',
    'Corporate Announcement',
    0,
    1,
    'sarbottam-cement-dividend-2024'
);

-- Insert sample financial data
INSERT INTO sarbottam_companyfinancial (
    company_id, report_period, total_revenue, net_income, earnings_per_share,
    total_assets, total_liabilities, shareholders_equity, report_date
) VALUES
(
    1,
    'Q3 2024',
    450.0,
    45.0,
    5.62,
    2500.0,
    800.0,
    1700.0,
    '2024-07-15'
),
(
    1,
    'Q2 2024',
    420.0,
    38.0,
    4.75,
    2450.0,
    750.0,
    1700.0,
    '2024-04-15'
),
(
    1,
    'Q1 2024',
    380.0,
    32.0,
    4.00,
    2400.0,
    720.0,
    1680.0,
    '2024-01-15'
);

-- Insert sample achievements
INSERT INTO sarbottam_companyachievement (
    company_id, title, description, achievement_date, category
) VALUES
(
    1,
    'First European Production Line in Nepal',
    'Sarbottam Cement became the first and only cement manufacturer in Nepal to implement a completely European production line, setting new industry standards.',
    '2012-06-15',
    'Technology Innovation'
),
(
    1,
    'ISO 9001:2015 Quality Certification',
    'Successfully obtained international quality management certification, demonstrating commitment to product quality and customer satisfaction.',
    '2018-03-20',
    'Quality Certification'
),
(
    1,
    'Best Cement Company Award 2023',
    'Recognized as the Best Cement Company by Nepal Chamber of Commerce for outstanding contribution to the construction industry.',
    '2023-11-10',
    'Industry Recognition'
),
(
    1,
    'Environmental Excellence Award',
    'Received recognition for environmental sustainability initiatives and commitment to eco-friendly manufacturing practices.',
    '2023-08-05',
    'Environmental'
);

-- Create indexes for better performance
CREATE INDEX idx_company_symbol ON sarbottam_company(symbol);
CREATE INDEX idx_news_date ON sarbottam_companynews(news_date);
CREATE INDEX idx_news_published ON sarbottam_companynews(is_published);
CREATE INDEX idx_financial_date ON sarbottam_companyfinancial(report_date);
CREATE INDEX idx_achievement_date ON sarbottam_companyachievement(achievement_date);

-- Display sample data
SELECT 'Database setup completed successfully!' as Status;
SELECT COUNT(*) as 'Total Companies' FROM sarbottam_company;
SELECT COUNT(*) as 'Total News Articles' FROM sarbottam_companynews;
SELECT COUNT(*) as 'Total Financial Records' FROM sarbottam_companyfinancial;
SELECT COUNT(*) as 'Total Achievements' FROM sarbottam_companyachievement;
