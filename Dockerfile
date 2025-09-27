FROM python:3.12-alpine

WORKDIR /opt/database-dataset

RUN apk add --no-cache gcc musl-dev g++ unixodbc-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh .
RUN chmod +x start.sh

ARG DB=mssql

RUN if [ "$DB" = "mssql" ]; then \
        wget -O msodbcsql17.apk https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.5.1-1_amd64.apk && \
        apk add --allow-untrusted msodbcsql17.apk && \
        rm msodbcsql17.apk && \
        echo "[ODBC Driver 17 for SQL Server]" > /etc/odbcinst.ini && \
        echo "Description=Microsoft ODBC Driver 17 for SQL Server" >> /etc/odbcinst.ini && \
        echo "Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.10.so.5.1" >> /etc/odbcinst.ini && \
        pip install --no-cache-dir pyodbc==5.2.0; \
    fi

RUN if [ "$DB" = "oracle" ]; then \
        pip install --no-cache-dir oracledb==3.3.0; \
    fi

ENV DB_TYPE=$DB

COPY src/ ./src/

ENTRYPOINT ["./start.sh"]