CREATE TABLE vacinations_per_country (
	"index" BIGINT, 
	country TEXT, 
	iso_code TEXT, 
	"date" TEXT, 
	total_vaccinations BIGINT, 
	people_vaccinated BIGINT, 
	people_fully_vaccinated BIGINT, 
	daily_vaccinations_raw FLOAT(53), 
	daily_vaccinations BIGINT, 
	total_vaccinations_per_hundred FLOAT(53), 
	people_vaccinated_per_hundred FLOAT(53), 
	people_fully_vaccinated_per_hundred FLOAT(53), 
	daily_vaccinations_per_million BIGINT, 
	vaccines TEXT, 
	source_name TEXT, 
	source_website TEXT
)