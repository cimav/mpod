USE giancarlo_mpod;
INSERT INTO data_publarticle (id, title, authors, journal, year, volume, issue, first_page, last_page, reference, pages_number) VALUES (1, 'Iron–Gallium Alloys', 'Jayasimha Atulasimha; Alison B Flatau', 'Magnetostrictive iron–gallium alloys', 2011, '?', '?', -1, -1, '?', -2);
INSERT INTO data_datafile (code, filename, cod_code, phase_generic, phase_name, chemical_formula, publication_id) VALUES (1000369, '1000369.mpod', -2, 'None', '?', 'FeGa', 1);
COMMIT;
