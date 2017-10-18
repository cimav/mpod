USE giancarlo_mpod;
INSERT INTO data_experimentalparcond (tag, description, name, units, units_detail) VALUES ('_prop_measurement_method', '_measurement_method', 'NULL', 'NULL', 'NULL');
UPDATE data_experimentalparcond SET name = 'measurement method' WHERE tag = '_prop_measurement_method';
UPDATE data_experimentalparcond SET units = 'n.a.' WHERE tag = '_prop_measurement_method';
UPDATE data_experimentalparcond SET units_detail = 'n.a.' WHERE tag = '_prop_measurement_method';
COMMIT;
