-- This script can be used to generate example users and training records in a freshly installed application.
-- It is not required to run the application otherwise.

-- Create example users
INSERT INTO users (first_name, last_name, email, password)
VALUES
    ('Alex',
    'Johnson',
    'alex.johnson@email.com',
    'scrypt:32768:8:1$T51VOw7gksdGt5JQ$c215526684cbe7476b8c800f72521a2e2d77a7f92bd432e6378eb7ee6ee76f46a7a5d5c4581c1c94e516ce233ac18de5e438cf8f5adff1297a2406bfe5b4673b'
    ),
    ('Sophia',
    'Smith',
    'sophia.smith@email.com',
    'scrypt:32768:8:1$VNO2Q63gfchyQfv1$f24a29e6b8b65f3ab76b925f59e3329c03903ef6a3015cae58ba299cf5aa04207e0583ab31916d5e47d8e11bf7c0bb187bfd10ee73157401cd9183f6f47c4ca2'
    ),
    ('John',
    'Davis',
    'john.davis@email.com',
    'scrypt:32768:8:1$mhTATfwPDIEBVGDi$962af5ba6f4f0548942a8ae5ef317585fc3fb8b80429c0437e7ccc6476c944893a01bea3aabe5cbd4bf659f7194e12ceace1d9a67e595a79f7f15af3e68b895a'
    ),
    ('Emma',
    'Brown',
    'emma.brown@email.com',
    'scrypt:32768:8:1$OcGnRlu0vzFPabAZ$a47dd8574ea57d8a927368889577467932519fde238100b66ef7647bc905c78d2cb5b0145f6abda1429789515e0d0f7e565a5ae4becfee1ce001a6643062d921'
    ),
    ('William',
    'White',
    'william.white@email.com',
    'scrypt:32768:8:1$Enj9pi0ys6Nqa4kq$38cbdd21823f282d3106a8ec5a039b9702948a57f8f8e5c7b7f9569247d7fef2736b14ce1e84c9ef24ebc744fa8feb79e3be7df2e1f4a16665e0b80ceab918ad'
    );

-- Create example course data
INSERT INTO training (user_id, course_name, category_id, date_completed, certification)
VALUES
    ((SELECT id FROM users WHERE email = 'alex.johnson@email.com'), 'Web Development Basics', 4, '2023-01-20', false),
    ((SELECT id FROM users WHERE email = 'sophia.smith@email.com'), 'Data Science Bootcamp', 3, '2022-12-05', true),
    ((SELECT id FROM users WHERE email = 'john.davis@email.com'), 'JavaScript Mastery', 4, '2023-01-15', false),
    ((SELECT id FROM users WHERE email = 'emma.brown@email.com'), 'Machine Learning Basics', 2, '2022-11-30', true),
    ((SELECT id FROM users WHERE email = 'william.white@email.com'), 'Mobile App Development', 5, '2023-01-10', false),
    ((SELECT id FROM users WHERE email = 'alex.johnson@email.com'), 'Cloud Computing Basics', 1, '2022-12-15', true),
    ((SELECT id FROM users WHERE email = 'sophia.smith@email.com'), 'Cyber Security Fundamentals', 2, '2023-01-05', false),
    ((SELECT id FROM users WHERE email = 'john.davis@email.com'), 'Database Management', 3, '2022-11-10', true),
    ((SELECT id FROM users WHERE email = 'emma.brown@email.com'), 'Full Stack Development', 4, '2023-01-01', false),
    ((SELECT id FROM users WHERE email = 'william.white@email.com'), 'Networking Essentials', 5, '2022-12-12', true),
    ((SELECT id FROM users WHERE email = 'alex.johnson@email.com'), 'Cloud Security', 2, '2022-11-28', false),
    ((SELECT id FROM users WHERE email = 'sophia.smith@email.com'), 'Advanced Data Analytics', 3, '2022-12-05', true),
    ((SELECT id FROM users WHERE email = 'john.davis@email.com'), 'Modern JavaScript Frameworks', 4, '2023-01-18', false),
    ((SELECT id FROM users WHERE email = 'emma.brown@email.com'), 'Deep Learning Concepts', 2, '2022-11-25', true),
    ((SELECT id FROM users WHERE email = 'william.white@email.com'), 'Mobile App UI/UX Design', 4, '2022-12-15', false),
    ((SELECT id FROM users WHERE email = 'alex.johnson@email.com'), 'Cloud Architecture', 1, '2022-11-10', true),
    ((SELECT id FROM users WHERE email = 'sophia.smith@email.com'), 'Cyber Threat Intelligence', 2, '2022-12-12', false),
    ((SELECT id FROM users WHERE email = 'john.davis@email.com'), 'Big Data Management', 3, '2022-12-02', true),
    ((SELECT id FROM users WHERE email = 'emma.brown@email.com'), 'Web Development Frameworks', 4, '2023-01-10', false),
    ((SELECT id FROM users WHERE email = 'william.white@email.com'), 'Network Security', 5, '2022-11-28', true);

