CREATE SCHEMA instruments;

CREATE TABLE instruments.guitars (
    id UUID PRIMARY KEY,
    make VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    type VARCHAR(255)
);

INSERT INTO instruments.guitars (id, make, model, type) VALUES ('b7337fa5-3e17-4628-b4db-00af02e07fdc', 'rickenbacker', '330', 'semi-hollow-electric');
