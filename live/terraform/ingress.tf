resource "kubernetes_ingress_v1" "ingress" {
  metadata {
    namespace   = data.kubernetes_namespace.default.metadata.0.name
    name        = local.base_name
    annotations = {
      "cert-manager.io/cluster-issuer" = "letsencrypt-prod"
      "kubernetes.io/ingress.class"    = "nginx"
      "kubernetes.io/tls-acme"         = "true"
    }
  }
  spec {
    rule {
      host = var.host
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.frontend_svc.metadata.0.name
              port {
                name = "http"
              }
            }
          }
        }
      }
    }
    tls {
      secret_name = "ingress-tls"
      hosts = [
        var.host
      ]
    }
  }
}

resource "kubernetes_ingress_v1" "www-redirect" {
  metadata {
    namespace   = data.kubernetes_namespace.default.metadata.0.name
    name        = "${local.base_name}-www-redirect"
    annotations = {
      "cert-manager.io/cluster-issuer" = "letsencrypt-prod"
      "kubernetes.io/ingress.class"    = "nginx"
      "kubernetes.io/tls-acme"         = "true"
      "nginx.ingress.kubernetes.io/configuration-snippet" = <<EOF
        location ~* /.* {
          return 301 https://${var.host};
        }
      EOF
    }
  }
  spec {
    rule {
      host = "www.${var.host}"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.frontend_svc.metadata.0.name
              port {
                name = "http"
              }
            }
          }
        }
      }
    }
    tls {
      secret_name = "ingress-tls"
      hosts = [
        var.host
      ]
    }
  }
}
