-- Data Skipping Index — 'minmax' ტიპი: ინახავს თითო data block-ის min/max
-- მნიშვნელობას rate-ზე, query-ს საშუალებას აძლევს, მთლიანად გამოტოვოს ის
-- block-ები, რომლებშიც ეძებული მნიშვნელობა ვერასდროს იქნება.
ALTER TABLE currency_rates
ADD INDEX IF NOT EXISTS idx_rate_minmax rate TYPE minmax GRANULARITY 4;

-- 'set' ტიპი — კარგია დაბალი cardinality-ის სვეტებზე (მაგ. currency_code,
-- თუ ის ORDER BY-ის ნაწილი არ იქნებოდა).
ALTER TABLE weather_events
ADD INDEX IF NOT EXISTS idx_city_set city TYPE set(100) GRANULARITY 4;

-- ინდექსი ავტომატურად ეხება მხოლოდ ახალ (ADD-ის შემდეგ ჩაწერილ) მონაცემს —
-- არსებულ ისტორიულ data-ზე გავრცელებისთვის საჭიროა MATERIALIZE.
ALTER TABLE currency_rates MATERIALIZE INDEX idx_rate_minmax;

-- გადამოწმება — EXPLAIN-ით ჩანს, რომელი index გამოიყენა query-მ
EXPLAIN indexes = 1
SELECT * FROM currency_rates WHERE rate > 2.9;
