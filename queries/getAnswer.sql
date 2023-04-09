select
    "text"
from
  :location m
ORDER BY
  COSINE_SIM(m.embedding, :question_embedding)
DESC
LIMIT 3