select
    "text"
from
    :location m
order by
    COSINE_SIM(m.embedding, :question_embedding)
desc
limit 3