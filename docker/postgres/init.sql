DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'sku') THEN
        CREATE TABLE public.sku
        (
            uuid uuid,
            marketplace_id integer,
            product_id bigint,
            title text,
            description text,
            brand text,
            seller_id integer,
            seller_name text,
            first_image_url text,
            category_id integer,
            category_lvl_1 text,
            category_lvl_2 text,
            category_lvl_3 text,
            category_remaining text,
            features json,
            rating_count integer,
            rating_value double precision,
            price_before_discounts real,
            discount double precision,
            price_after_discounts real,
            bonuses integer,
            sales integer,
            inserted_at timestamp default now(),
            updated_at timestamp default now(),
            currency text,
            barcode bigint,
            similar_sku uuid[]
        );

        -- Добавляем комментарии к столбцам
        COMMENT ON COLUMN public.sku.uuid IS 'id товара в нашей бд';
        COMMENT ON COLUMN public.sku.marketplace_id IS 'id маркетплейса';
        COMMENT ON COLUMN public.sku.product_id IS 'id товара в маркетплейсе';
        COMMENT ON COLUMN public.sku.title IS 'название товара';
        COMMENT ON COLUMN public.sku.description IS 'описание товара';
        COMMENT ON COLUMN public.sku.category_lvl_1 IS 'Первая часть категории товара. Например, для товара, находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и игры/Игровые консоли, в это поле запишется "Детям".';
        COMMENT ON COLUMN public.sku.category_lvl_2 IS 'Вторая часть категории товара. Например, для товара, находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и игры/Игровые консоли, в это поле запишется "Электроника".';
        COMMENT ON COLUMN public.sku.category_lvl_3 IS 'Третья часть категории товара. Например, для товара, находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и игры/Игровые консоли, в это поле запишется "Детская электроника".';
        COMMENT ON COLUMN public.sku.category_remaining IS 'Остаток категории товара. Например, для товара, находящегося по пути Детям/Электроника/Детская электроника/Игровая консоль/Игровые консоли и игры/Игровые консоли, в это поле запишется "Игровая консоль/Игровые консоли и игры/Игровые консоли".';
        COMMENT ON COLUMN public.sku.features IS 'Характеристики товара';
        COMMENT ON COLUMN public.sku.rating_count IS 'Кол-во отзывов о товаре';
        COMMENT ON COLUMN public.sku.rating_value IS 'Рейтинг товара (0-5)';
        COMMENT ON COLUMN public.sku.barcode IS 'Штрихкод';

        -- Создаем индексы с использованием IF NOT EXISTS
        CREATE INDEX IF NOT EXISTS sku_brand_index ON public.sku (brand);
        CREATE UNIQUE INDEX IF NOT EXISTS sku_marketplace_id_sku_id_uindex ON public.sku (marketplace_id, product_id);
        CREATE UNIQUE INDEX IF NOT EXISTS sku_uuid_uindex ON public.sku (uuid);
    END IF;
END $$;