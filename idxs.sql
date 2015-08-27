CREATE INDEX tenders_plangraphposition_state_idx
	ON tenders_plangraphposition
	USING btree
	(state);

CREATE INDEX tenders_plangraphposition_number_idx
	ON tenders_plangraphposition
	USING btree
	(number);