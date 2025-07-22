-- Create database
CREATE DATABASE IF NOT EXISTS sarbottam_cement_db;
USE sarbottam_cement_db;

-- Company profile table
CREATE TABLE IF NOT EXISTS company_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    stock_symbol VARCHAR(10) NOT NULL,
    company_logo VARCHAR(255),
    established_year INT,
    company_type VARCHAR(100),
    sector VARCHAR(100),
    industry VARCHAR(100),
    headquarters VARCHAR(255),
    total_employees INT,
    market_cap DECIMAL(15, 2),
    paid_up_capital DECIMAL(15, 2),
    authorized_capital DECIMAL(15, 2),
    current_share_price DECIMAL(10, 2),
    total_shares BIGINT,
    listed_shares BIGINT,
    website_url VARCHAR(255),
    email VARCHAR(100),
    phone VARCHAR(50),
    chairman_name VARCHAR(255),
    ceo_name VARCHAR(255),
    company_description TEXT,
    key_products TEXT,
    production_capacity VARCHAR(255),
    plant_locations TEXT,
    vision_statement TEXT,
    mission_statement TEXT,
    core_values TEXT,
    financial_year VARCHAR(20),
    annual_revenue DECIMAL(15, 2),
    net_profit DECIMAL(15, 2),
    eps DECIMAL(10, 2),
    book_value DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- News table
CREATE TABLE IF NOT EXISTS company_news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    news_title VARCHAR(500) NOT NULL,
    news_date DATE NOT NULL,
    news_image VARCHAR(255),
    news_body TEXT NOT NULL,
    news_summary TEXT,
    news_category VARCHAR(100),
    is_featured BOOLEAN DEFAULT FALSE,
    views_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample company data for Sarbottam Cement Limited
INSERT INTO company_profile (
    company_name, stock_symbol, established_year, company_type, sector, industry,
    headquarters, total_employees, paid_up_capital, authorized_capital,
    website_url, email, phone, chairman_name, ceo_name,
    company_description, key_products, production_capacity, plant_locations,
    vision_statement, mission_statement, core_values
) VALUES (
    'Sarbottam Cement Limited',
    'SARBTM',
    2010,
    'Public Limited Company',
    'Manufacturing and Processing',
    'Cement Manufacturing',
    'Sunwal, Nawalparasi, Gandaki Province, Nepal',
    850,
    2500000000.00,
    5000000000.00,
    'https://saurabhgroup.com/sarbottam-cement',
    'info@saurabhgroup.com',
    '+977-78-402001',
    'Mr. Saurabh Kumar Agrawal',
    'Mr. Rajesh Kumar Sharma',
    'Sarbottam Cement Limited (SCPL) is an innovator and pioneer of the cement industry of Nepal. It is the first and only cement manufacturer in Nepal to use a completely European production line. The company is committed to providing high-quality cement products that meet international standards while contributing to Nepal''s infrastructure development.',
    'Ordinary Portland Cement (OPC), Portland Pozzolana Cement (PPC), Composite Cement, Special Purpose Cement',
    '3,000 Metric Tons Per Day',
    'Main Plant: Sunwal, Nawalparasi; Distribution Centers: Kathmandu, Pokhara, Chitwan, Butwal',
    'To be the most trusted cement manufacturer in Nepal, leading the industry through innovation, quality, and sustainable practices.',
    'To provide superior quality cement products that contribute to Nepal''s infrastructure development while maintaining environmental sustainability and creating value for all stakeholders.',
    'Quality Excellence, Environmental Sustainability, Innovation, Customer Focus, Integrity, Community Development'
);

-- Insert sample news data
INSERT INTO company_news (news_title, news_date, news_body, news_summary, news_category, is_featured) VALUES
(
    'Sarbottam Cement Reports Strong Q3 Financial Performance',
    '2025-01-15',
    'Sarbottam Cement Limited announced its third quarter financial results, showing a significant increase in revenue and profitability. The company reported a 25% increase in net sales compared to the same period last year, driven by increased demand in the construction sector and improved operational efficiency.

    The company''s cement production reached 820,000 metric tons during the quarter, representing a 15% increase from the previous year. This growth was attributed to the successful implementation of European production line technology and improved supply chain management.

    "We are pleased with our strong performance this quarter," said CEO Mr. Rajesh Kumar Sharma. "Our focus on quality and customer satisfaction continues to drive growth, and we remain optimistic about the future prospects of Nepal''s construction industry."

    The company also announced plans to expand its distribution network and invest in renewable energy projects to reduce its carbon footprint. These initiatives align with the company''s commitment to sustainable development and environmental responsibility.',
    'Sarbottam Cement reports 25% increase in Q3 revenue and announces expansion plans for distribution network and renewable energy projects.',
    'Financial',
    TRUE
),
(
    'New Partnership with Leading Construction Companies',
    '2025-01-10',
    'Sarbottam Cement Limited has entered into strategic partnerships with several leading construction companies across Nepal to strengthen its market position and improve service delivery to customers.

    The partnerships include agreements with major infrastructure developers working on government projects, including highway construction, bridge building, and urban development initiatives. These collaborations will ensure a steady supply of high-quality cement for critical infrastructure projects.

    "These partnerships represent our commitment to supporting Nepal''s infrastructure development," commented Chairman Mr. Saurabh Kumar Agrawal. "By working closely with construction companies, we can better understand market needs and provide customized solutions."

    The company has also announced the launch of a new customer service initiative that includes technical support, on-site consultation, and quality assurance services. This comprehensive approach aims to strengthen customer relationships and ensure project success.

    As part of the partnership agreements, Sarbottam Cement will provide specialized cement grades for different construction applications, ensuring optimal performance and durability for various project requirements.',
    'Sarbottam Cement forms strategic partnerships with leading construction companies to strengthen market position and support infrastructure development.',
    'Business',
    TRUE
),
(
    'Environmental Sustainability Initiative Launched',
    '2025-01-05',
    'Sarbottam Cement Limited has launched a comprehensive environmental sustainability initiative aimed at reducing its carbon footprint and promoting eco-friendly practices throughout its operations.

    The initiative includes several key components: implementation of alternative fuel technologies, installation of dust collection systems, water conservation measures, and afforestation programs in surrounding communities.

    The company has committed to achieving a 30% reduction in CO2 emissions by 2030 through the use of alternative fuels and energy-efficient production processes. This goal aligns with global climate targets and demonstrates the company''s commitment to environmental stewardship.

    "Environmental responsibility is at the core of our business philosophy," stated the company''s Environment Manager. "We believe that sustainable practices not only benefit the environment but also create long-term value for our stakeholders."

    The company has also announced plans to invest in solar energy systems for its manufacturing facilities and implement waste heat recovery systems to improve energy efficiency. These investments are expected to reduce operational costs while contributing to environmental protection.',
    'Sarbottam Cement launches environmental sustainability initiative targeting 30% CO2 reduction by 2030 through alternative fuels and energy efficiency measures.',
    'Environment',
    FALSE
),
(
    'Technology Upgrade Enhances Production Efficiency',
    '2024-12-28',
    'Sarbottam Cement Limited has completed a major technology upgrade at its Sunwal manufacturing facility, implementing advanced automation systems and quality control measures that significantly enhance production efficiency and product quality.

    The upgrade includes installation of state-of-the-art European equipment for grinding, mixing, and packaging operations. These improvements have resulted in a 20% increase in production capacity and improved consistency in product quality.

    The new technology features automated monitoring systems that continuously track production parameters and ensure optimal performance. Real-time data analysis capabilities enable rapid response to any variations in production conditions.

    "This technology upgrade represents a significant milestone in our journey toward operational excellence," said the company''s Technical Director. "The new systems not only improve efficiency but also enhance our ability to maintain the highest quality standards."

    The company has also implemented predictive maintenance systems that use data analytics to anticipate equipment maintenance needs, reducing downtime and extending equipment life. These improvements are expected to generate significant cost savings and improve overall operational reliability.',
    'Sarbottam Cement completes major technology upgrade featuring European equipment and automation systems, increasing production capacity by 20%.',
    'Technology',
    FALSE
);

-- Create indexes for better performance
CREATE INDEX idx_company_stock_symbol ON company_profile(stock_symbol);
CREATE INDEX idx_news_date ON company_news(news_date);
CREATE INDEX idx_news_category ON company_news(news_category);
CREATE INDEX idx_news_featured ON company_news(is_featured);
